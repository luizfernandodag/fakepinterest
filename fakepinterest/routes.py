import time

from fakepinterest import app, database, bcrypt
from flask import render_template, url_for, request
from flask_login import login_required, login_user, logout_user,current_user
from flask import redirect
from fakepinterest.models import Usuario, Foto
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.utils import secure_filename

#@app.route("/", methods=["GET", "POST"])
#def homepage():
#   form_login = FormLogin()
#    print("A")
#    print(form_login.validate_on_submit())
#    if form_login.validate_on_submit():

#        print("B")
    #if request.method == 'POST':
#        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
#        print(usuario.username)
#        print("C")
#        if usuario:
#            if bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
#                print("D")
#                login_user(usuario)
#                return redirect(url_for("perfil", usuario=usuario.username))
#    else:
#       print(form_login.errors)

#    print(form_login.validate_on_submit())
#    return render_template("homepage.html", form=form_login)


@app.route("/", methods = ["GET","POST"])
def homepage():
    form_login = FormLogin(request.form)
    print(form_login.validate_on_submit())
    if request.method == 'POST': #and form_login.validate():
        print(form_login.email.data)
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario == None:
            print("None")
        else:
            print("usuario.username: "+usuario.username)
            if bcrypt.check_password_hash(usuario.senha,form_login.senha.data):
                login_user(usuario)
                return redirect(url_for("perfil", id_usuario=usuario.id))



    return render_template("homepage.html", form=form_login)

@app.route('/logout')
@login_required
def logout():
    logout(current_user)
    return redirect(url_for("homepage"))



@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    print(request.method)
    print(form_criarconta.validate_on_submit())
    if request.method == 'POST':
        #if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        #print(form_criarconta.username.data)
        #print(senha)
        #print(form_criarconta.email.data)
        usuario = Usuario(username=form_criarconta.username.data,
                              senha=senha,
                              email=form_criarconta.email.data)
        try:
            #print("AQUI1")
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario,remember=True)
            return redirect(url_for("perfil",id_usuario=usuario.id))  # Redirect after successful form submission
        except SQLAlchemyError as e:
            database.session.rollback()
            print(f"Database error: {str(e)}")
        #else:
            #print("não entrou if 2")

    else:
        print("não entrou if 1")

    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET","POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()

        if request.method == 'POST' and form_foto.validate_on_submit():

            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            #salvar na pasta
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   #r'\static\fotos_posts',
                                   app.config['UPLOAD_FOLDER'],
                              nome_seguro)
            print(caminho)

            # registrar no banco
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        else:
            print("ERRO")





        return render_template("perfil.html", usuario = current_user, form = form_foto)
    else:
        usuario = Usuario.query.get(id_usuario)
        return render_template("perfil.html", usuario = usuario, form = None)


@app.route("/feed")
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all()
    return render_template("feed.html",fotos=fotos)