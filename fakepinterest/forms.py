from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from fakepinterest.models import Usuario
from fakepinterest import bcrypt

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    botao_confirmacao = SubmitField('Fazer Login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Usuario não cadastrado - Crie uma conta')

    def validate_senha(self, senha):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if usuario:
            if not bcrypt.check_password_hash(usuario.senha.encode("utf-8"), senha.data):
                raise ValidationError('Senha Incorreta')




class FormCriarConta(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Nome Usuario', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6,max=20)])
    confirmacao_senha = PasswordField('Confirma senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email ja cadatrado faça login para continuar')


class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired(), FileAllowed(["jpeg","jpg", "png"])])
    botao_confirmacao = SubmitField('Enviar Foto')
