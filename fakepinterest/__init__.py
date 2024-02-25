from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/local'  # Update with your MySQL database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://banco_fakepinterest_xrsn_user:c2feKZOZKjSmuvNDQLzutfSFKv8qarv8@dpg-cnd8v86g1b2c739litp0-a.oregon-postgres.render.com/banco_fakepinterest_xrsn"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databasename'  # Update with your MySQL database credentials

app.config["SECRET_KEY"] = "59d3e5bf433a5789c3dca5ff53c15983"
app.config["UPLOAD_FOLDER"] = r"static\fotos_posts"


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fakepinterest import routes





