from app import app, db
from flask import jsonify, request
from auth import auth
from models import Comment, Post


# post
@app.route('/post-story', methods=['POST'])
@auth.login_required
def post():
    data = request.json
    current_user = auth.current_user()
    post = data.get('post')
    
    if post is None:
        return jsonify({'error': "input words"})
    
    new_post = Post(post=post, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'done': True, 'message': 'Post successful'}), 200
    

# post  comment
@app.route('/comment', methods=['POST'])
@auth.login_required
def comment():
    data = request.json
    current_user = auth.current_user()
    post_id = data.get('post_id')
    content = data.get('content')
    
    if content is None or post_id is None:
        return jsonify({'error': 'Post ID and content are required.'}), 400
    
    post = Post.query.get(post_id)
    
    if post is None:
        return jsonify({'error': "Post not found"}), 404
    
    new_comment = Comment(post_id=post_id, user_id=current_user.id, content=content)
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({'done': True, 'message': 'Comment added successfully'}), 200
