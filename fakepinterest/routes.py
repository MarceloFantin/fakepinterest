#criar as rotas/links dos site
import flask_login
from flask import render_template, url_for, redirect
from fakepinterest import app, bcrypt, database
from flask_login import login_required, current_user, login_user, logout_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename



@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template('homepage.html', formlogin=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha_crypt = bcrypt.generate_password_hash(formcriarconta.senha.data).decode('utf-8')
        usuario = Usuario(username=formcriarconta.username.data,
                          email=formcriarconta.email.data,
                          senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario)
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criarconta.html', formcriarconta=formcriarconta)


@app.route('/perfil/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if id_usuario == int(current_user.id):
        #usuario esta vendo o proprio perfil
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            print(arquivo)
            nome_seguro = secure_filename(arquivo.filename)
            nome, extencao = os.path.splitext(nome_seguro)
            nome_arquivo = nome + "_" + str(current_user.id) + extencao
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config['UPLOAD_FOLDER'],
                              nome_arquivo)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_arquivo, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for('perfil', id_usuario=id_usuario))

        return render_template('perfil.html', usuario=current_user, formfoto=formfoto)
    else:
        #usuario esta vendo perfil de outros
        usuario = Usuario.query.get_or_404(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, formfoto=None)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    print(len(fotos))
    return render_template('feed.html', fotos=fotos)
