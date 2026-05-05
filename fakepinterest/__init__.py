from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os



app = Flask(__name__)

#para criacao do banco de dados de forma remota
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://banco_fakepinterest_y9yo_user:2zio2YJGTB76p0WO4YiHGn2TnAymzess@dpg-d7sji5rbc2fs73cqnvpg-a.virginia-postgres.render.com/banco_fakepinterest_y9yo"

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config["SECRET_KEY"] = "3tvh17ihwt0vtrXnBuDHQw"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"



database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'




from fakepinterest import routes
