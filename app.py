from flask import Flask 
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from extensions import db
from config import Config
from auth import delete_old_posts, delete_old_comments
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app=app, db=db)
mail = Mail(app)
cors = CORS(resources={r"/*": {"origins": "*"}}, app=app)

from routes import users
from routes import post


# delete post
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old_posts, trigger="interval", hours=1)
# delete comment
scheduler.add_job(func=delete_old_comments, trigger="interval", hours=1)
scheduler.start()