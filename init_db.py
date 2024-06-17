from ext import app, db
from models import Post

with app.app_context():
    db.drop_all()
    db.create_all()
    
    