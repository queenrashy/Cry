
import re
import string
import random
from PIL import Image, ImageDraw

from flask_mail import Message
from app import mail
from config import Config
def is_valid_email(email):
    if email is None:
        return False
    # Regular expression pattern for validating an email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
    
    # Match the email against the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
    
    
# generate a random number for the token
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# generate user name
def random_username(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# generate images
def generate_random_image(image_path):
    width, height = 300, 300
    img = Image.new('RGB', (width, height), color=(random.randint(0, 255), random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    draw = ImageDraw.Draw(img)
    
    # draw some random shapes or text
    draw.line((0,0) + img.size, fill=(255, 255, 255), width=5)
    draw.line((0, img.size[1], img.size[0], 0), fill=(255, 255, 255), width=5)
    
    # save the image with a unique name
    img.save(f"random_image{random.randint(1000,9999)}.png")

# send email function
def send_email(subject, receiver, text_body, html_body):
    msg = Message(subject=subject, sender=('Queen', Config.MAIL_USERNAME), recipients=[receiver])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

