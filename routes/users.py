import os
import random
from app import app, db
from flask import jsonify, request
from auth import auth
from datetime import datetime, timedelta
from models import User, PasswordResetToken, StoredjwtToken
from toolz import random_username, generate_random_image, send_email, is_valid_email, random_generator

# signup user
@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # check email if valid
    if not is_valid_email(email):
        return jsonify({'error': 'Please enter a valid email address'}), 400
    
    # check unique email
    email_exist = User.query.filter(User.email == email).first()
    if email_exist is not None:
        return jsonify({'error': 'Email already exists'}), 400
    
    #  strong password
    if password is None or len(password) < 8:
        return jsonify({'error': 'Password is invalid, please enter 8 or more characters'})
    
    # generate random username 
    username = random_username()
    
    # Generate random image and save it 
    image_filename = f"{username}.png"
    image_path = os.path.join('static', 'images', image_filename)
    generate_random_image(image_path)
    
    # save to database
    new_user = User(email=email,username=username, image=image_filename)
    db.session.add(new_user)
    new_user.set_password(password)
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'Created': 'Account created Successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'User signup error: {e}'}), 400
    
@app.route('/login', methods=['GET'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # validate input
    if email is None or password is None:
        return jsonify({'error': 'Please enter a valid email or password'}), 400
    
    # validate email
    if not is_valid_email(email):
        return jsonify({'error': 'Please enter a valid email address'}), 400
    
    # find user
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'error': 'User with this email does not exist'}), 401
    
    # validate password
    if user.check_password(password):
        # delete previous token
        saved_token = StoredjwtToken.query.filter_by(user_id = user.id).first()
        if saved_token is not None:
            db.session.delete(saved_token)
            
        # password is correct, generate jwt token
        token = user.generate_auth_token()
        new_jwt_token = StoredjwtToken(user_id=user.id, jwt_token=token)
        db.session.add(new_jwt_token)
        db.session.commit()
        return jsonify({'success': True, 'token': token}), 200
    return jsonify({'error': 'Invalid email or password.'}), 400
    
    
# User logout
@app.route('/logout', methods=['GET'])
@auth.login_required 
def logout():
    user = auth.current_user()
    user_id = user.id
    active_token = StoredjwtToken.query.filter_by(user_id=user_id).first()
    db.session.delete(active_token)
    db.session.commit()
    
    # send logout email
    subject = 'Logout Notification'
    text_body = f'Hi {user.fullName}, \n\nYou have successfully logged out of your account.'
    html_body = f" <h3> Hello {user.fullName}, </h3> <p> You have just <strong> logged out </strong> of your account. <p> if this wasn't you, please log in and change your password immediately. </p>"
    
    send_email(subject=subject, receiver=user.email, text_body=text_body, html_body=html_body)
    
    return jsonify({'success': True, 'message': 'User logout successfully'})
     
     
# forget password
@app.route('/forget-password', methods=['POST'])
def forget_password():
    email = request.json.get('email')
    
    # if email exist
    if email is None:
        return jsonify({'error': 'Please enter email'}), 400
    
    user = User.query.filter_by(email=email). first()
    if user is None:
        return jsonify({'error': 'User with this email does not exist'}), 400
    
    # create a password reset token
    token = random_generator(8)
    reset = PasswordResetToken(token=token, user_id=user.id, used=False) 
    db.session.add(reset)
    db.session.commit()
    
    # send password reset token to email
    return jsonify({'success': True, 'message': 'Password reset email sent'}), 200 

# reset password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.json.get('token')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')
    
    if new_password is None or confirm_password != new_password:
        return jsonify({'error': 'Password does not match'}), 400
    
    if token is None:
        return jsonify({'error': 'Please enter token'}), 400
    
    reset = PasswordResetToken.query.filter_by(token=token).first()
    
    if reset is None:
        return jsonify({'error': 'Invalid token'}), 400
    
    if reset.used:
        return jsonify({'error': 'Token has been used already'}), 400
    
    user = User.query.filter_by(id=reset.user_id).first()
    
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    
    user.set_password(new_password)
    reset.used = True
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Password reset successfully'}), 200
    
   
# delete user account  
@app.route('/<int:did>', methods=['DELETE'])
@auth.login_required
def delete_user(did):
    # user = auth.current_user()
    user = User.query.filter(User.id == did).first()
    if user is None:
        return jsonify({'error': 'User does not exit'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'done': True, 'message': f'{user.email } Account deleted successfully!'}) 


# update user profile
@app.route('/profile')
@auth.login_required
def user_profile():
    user = auth.current_user()
    
    now = datetime.utcnow()
    if user.last_image_update is None or now - user.last_image_update > timedelta(hours=24):
        # generate  unique new image filename
        unique_number = random.randint(1000,9999)
        image_filename = f"{user.username}_{unique_number}.png"
        image_path = os.path.join('static', 'images', image_filename)
        generate_random_image(image_path)
        
        # update timestamp
        user.image = image_filename
        user.last_image_update = now
        db.session.commit()
        
        return jsonify({
            "username": user.username,
            "image": user.image,
            "email": user.email
        })