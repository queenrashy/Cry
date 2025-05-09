from flask import make_response, jsonify
from extensions import db
from datetime import datetime, timedelta
from models import Comment, Post
from models import User

from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')

    
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Authorized access'}), 401)

@auth.verify_token
def verify_token(token):
    return User.verify_auth_token(token)

# delete post 
def delete_old_posts():
    expiry_time = datetime.utcnow() - timedelta(hours=24)
    expired_posts = Post.query.filter(Post.post_date < expiry_time).all()
    for post in expired_posts:
        db.session.delete(post)
    db.session.commit()
    
    
# delete comment
def delete_old_comments():
    # get current time
    now = datetime.utcnow
    
    # find all comments older than 24 hours
    old_comments = Comment.query.filter(Comment.comment_date < now - timedelta(days=1)).all()
    
    # delete each old comment
    for comment in old_comments:
        db.session.delete(comment)
        
    # commit changes
    db.session.commit()
    