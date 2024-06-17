from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db, login_manager



class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def save():
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    __tablename__="users"
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(),nullable=False)
    password = db.Column(db.String())
    name = db.Column(db.String())
    role = db.Column(db.String(), default="user")
    def __init__(self, username, password,name, role="user"):
        self.username = username
        self.name = name
        self.password = generate_password_hash(password)
        self.role = role
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(db.Model, BaseModel):
    
    __tablename__="posts"
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    title = db.Column(db.String(),nullable=True, default="Untitled")
    img = db.Column(db.String(), default="default.jpg")
    comment = db.Column(db.String())
    like_count = db.Column(db.Integer(),default=0)
    def __repr__(self):
        return self.title
    

    

    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 


class PostComment(db.Model, BaseModel):
    __tablename__="post_comments"
    
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    sub = db.Column(db.String())
    text = db.Column(db.String())

class Like(db.Model, BaseModel):
    __tablename__="likes"
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    post = db.relationship("Post")

