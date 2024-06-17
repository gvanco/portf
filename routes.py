from flask import  render_template, redirect, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from forms import PostFrom, SignupForm, LoginForm, PostCommentForm, LikeForm
from ext import app, db
from models import Post, User, BaseModel, PostComment, Like


@app.route("/login", methods = ["POST", "GET"])
def login():
    form = LoginForm()
    success = True
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            success = True
            login_user(user)
            return redirect("/")
        else: success = False
            
    return render_template("login.html", form=form, suc=success)




@app.route("/logout", methods = ["POST", "GET"])
def logout():
    logout_user()
    return redirect("/")

@app.route("/signup", methods = ["GET","POST"])
def signup():
    form = SignupForm()
    # 0 --> no info
    # 1 --> username is taken
    # 2 --> username is NOT taken
    username_taken=0
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user:
            username_taken = 1
            print("not suc")
        if not user:
            print("suc")
            username_taken = 2
            new_user = User(username=form.username.data,name=form.name.data,password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
        return render_template("signup.html", msg=username_taken, form=form)
    return render_template("signup.html", form=form)


@app.route("/create", methods = ["POST","GET"])
@login_required
def create():
    form = PostFrom()

    if form.validate_on_submit():
        image = form.post_pic.data
        # print(Post.img, "\n", image.filename)

        new_post = Post(title=form.title.data, comment=form.comment.data, user_id=current_user.id)
        if image:
            directory = path.join(app.root_path, "static", "images","pics", image.filename)
            image.save(directory)
            new_post.img = image.filename
        db.session.add(new_post)
        db.session.commit()
        return redirect("/")
    return render_template("create.html", form=form)

@app.route("/profile")
@login_required
def profile_page():
    return render_template("profile.html")

@app.route("/post/<int:post_id>", methods = ["POST", "GET"])
# @login_required
def post(post_id):
    form = PostCommentForm()
    pic = Post.query.get(post_id)
    comments = PostComment.query.filter(PostComment.post_id==post_id).all()
    like= Like.query.filter(current_user.id == Like.user_id).first()
    user = User.query.all()
    lform = LikeForm()
    already_liked = 0
    # 0 --> no info
    # 1 --> not liked
    # 2 --> already liked
    if current_user.is_authenticated:
        role = current_user.role
        admin = role=="admin"
        if form.validate_on_submit():
            new_comment = PostComment(sub=form.sub.data, text = form.text.data, post_id=post_id, user_id=current_user.id)
            new_comment.create()
            return redirect(f"/post/{post_id}")
        if lform.validate_on_submit():
            if pic.user_id == current_user.id:
                pass
                print("idk") 
            else:
                if like:
                    like.delete()
                    pic.like_count -= 1
                    pic.save()
                    already_liked = 1
                else:
                    Like(post_id=post_id, user_id=current_user.id).create()
                    pic.like_count += 1
                    already_liked = 2
                    pic.save()
            return redirect(f"/post/{post_id}")
    else:
        admin = False
    return render_template("post.html",  pic=pic, admin=admin, comments=comments, form=form, user=user, lform=lform, already_liked=already_liked, like=like)

@app.route("/post/<int:post_id>/delete")
def post_delete(post_id):
    pic = Post.query.get(post_id)
    pic.delete()
    return redirect("/")

@app.route("/post/<int:post_id>/edit", methods =["GET","POST"])
def post_edit(post_id):
    pic = Post.query.get(post_id)
    form = PostFrom(title=pic.title, comment=pic.comment, post_pic=pic.img)
    image=form.post_pic.data
    if form.validate_on_submit():
        pic.title=form.title.data
        pic.comment=form.comment.data
        if form.post_pic.data != pic.img:
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            pic.img = image.filename
        pic.save()
        return redirect(f"/post/{post_id}")
    return render_template("create.html", form=form)

@app.route("/post/<int:post_id>/comment/delete/<int:comm_id>")
def comment_delete(post_id,comm_id):
    comment=PostComment.query.get(comm_id)
    comment.delete()
    return redirect(f"/post/{post_id}")

@app.route("/post/<int:post_id>/comment/edit/<int:comm_id>", methods =["GET","POST"])
def comment_edit(post_id,comm_id):
    comment=PostComment.query.get(comm_id)
    form = PostCommentForm(sub=comment.sub, text=comment.text)
    if form.validate_on_submit():
        comment.sub=form.sub.data
        comment.text=form.text.data
        comment.save()
        return redirect(f"/post/{post_id}")
    return render_template("commentedit.html", comment=comment, form=form)


        
@app.route("/" ,methods=["GET", "POST"])
def home():
    pics = Post.query.all()
    user=User.query.all()
    lform = LikeForm()
    liked = None    
    if current_user.is_authenticated:
        all_likes= Like.query.filter(current_user.id == Like.user_id).all()
        liked_posts=[like.post for like in all_likes]
        # print(liked_posts)
        role = current_user.role
        admin = role=="admin"
        if lform.validate_on_submit():
            post_id = lform.post_id.data
            liked= Like.query.filter(current_user.id == Like.user_id, post_id == Like.post_id).first()
            pic = Post.query.get(post_id)
            if pic.user_id != current_user.id:
                if liked:
                    liked.delete()
                    pic.like_count -= 1
                    pic.save()
                else:
                    Like(post_id=post_id, user_id=current_user.id).create()
                    pic.like_count += 1
                    pic.save()
            return redirect("/")
    else:
        admin = False
        liked_posts=[]
    return render_template("home.html", pics=pics, admin=admin, user=user, liked=liked, liked_posts=liked_posts, lform=lform, User=User)        

@app.route("/about")
def news():
    return render_template("about.html")

