#criar as rotas/links dos site
from flask import render_template, url_for, redirect, send_from_directory
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
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):
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


@app.route("/upload/<path:filename>", methods=['GET', 'POST'])
def custom_static(filename):
    #1 -  para usar essa função tem que colocar o REDER como pago e criar uma pasta fixa fora do projeto como /fotos_posts
    #2 - no __init__.py tem que mudar a app.config["UPLOAD_FOLDER"] = "static/fotos_posts" para app.config["UPLOAD_FOLDER"] = "/fotos_posts"
    #3 - e no perfil.html e no feed.html nas linhas que carregam a imagem tem que mudar
    #de    <img src="{{ url_for('static', filename='fotos_posts/{}'.format(foto.imagem)) }}">
    #para  <img src="{{ url_for('custom_static', filename='{}'.format(foto.imagem)) }}">
    #4 - no routes.py a linha
    #de   - caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
    #                            app.config['UPLOAD_FOLDER'],
    #                            nome_arquivo)
    #para - caminho = os.path.join(app.config['UPLOAD_FOLDER'],
    #                              nome_arquivo)
    #
    #isso resolveria o problema de as imagens sumirem quando o render faz um deploy ou algo que cria novamente as pastas
    #porque as pastas são afemeras e todas as vezes são criadas novamente
    #da para criar um logica para saber se o projeto esta no ar ou no arquivo local para seguir sempre o caminho
    #correto tipo criar uma variavel de ambiente no servidor para fazer essa configuração
    #igual quando pega o banco de dados local ou o que esta na servidor.
    #isso não será feito pois o plano do RENDER é o free
    return os.path.join(app.config["UPLOAD_FOLDER"], filename, as_attachement=True)


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
