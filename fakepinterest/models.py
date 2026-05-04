from fakepinterest import database, login_manager
from datetime import datetime, timezone
from flask_login import  UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = database.Column(database.String(80), nullable=False)
    email = database.Column(database.String(80), nullable=False, unique=True)
    senha = database.Column(database.String(80), nullable=False)
    fotos = database.Relationship("Foto", backref="usuario", lazy=True)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True, nullable=False)
    imagem = database.Column(database.String(80), default = "default.jpg")
    data_criacao = database.Column(database.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)