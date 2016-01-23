#!/usr/bin/env python
from flask import Flask, g, jsonify
from flask.ext.script import Manager,Server
from api.app import create_app
from api.models import db, Usuario

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
    db.create_all()
    user = Usuario(name="admin",email="admin@admin",username="teste", password="teste")
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format("teste"))    

@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=api', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover','--exe'])


if __name__ == '__main__':
    manager.run()
