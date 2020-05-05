#!/usr/bin/env python
from flask import Flask, g, jsonify
from flask_script import Manager,Server
from api.app import create_app
from api.models import db, Usuario,Perfil

manager = Manager(create_app)
manager.add_command("runserver", Server(host='0.0.0.0'))

@manager.command
def createdb():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

@manager.command
def adduser(username):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = Usuario(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))

@manager.command
def addadmin():
    """Register admin user."""
    user = Usuario(nome="admin",email="admin@admin",nome_guerra="admin",username="teste", password="teste")
    db.session.add(user)
    user.add_perfis([Perfil.ADMINISTRADOR,Perfil.ESCALANTE])
    db.session.commit()
    print('User {0} was registered successfully.'.format("teste"))

@manager.command
def populatedb():
    """Register admin user."""
    users = [Usuario(nome="miranda",nome_guerra="miranda" ,email="miranda@intranet",username="miranda", password="miranda"), \
            Usuario(nome="claudio",nome_guerra="claudio" ,email="claudio@intranet",username="claudio", password="claudio"), \
            Usuario(nome="joao",nome_guerra="joao" ,email="joao@intranet",username="joao", password="joao"), \
            Usuario(nome="marcele",nome_guerra="marcele" ,email="marcele@intranet",username="marcele", password="marcele"), \
            Usuario(nome="juliana",nome_guerra="juliana" ,email="juliana@intranet",username="juliana", password="juliana"), \
            Usuario(nome="marta",nome_guerra="marta" ,email="marta@intranet",username="marta", password="marta"), \
            Usuario(nome="renata",nome_guerra="renata" ,email="renata@intranet",username="renata", password="renata"), \
            Usuario(nome="ana",nome_guerra="ana" ,email="ana@intranet",username="ana", password="ana")]
    db.session.add_all(users)
    db.session.commit()
    print('Users were registered successfully.')

@manager.command
def test():
    from subprocess import call
    #nosetests -v --with-coverage --cover-package=api --cover-branches --cover-erase --cover-html --cover-html-dir=cover --exe
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=api', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover','--exe'])



if __name__ == '__main__':
    app = create_app()
    manager.run()
