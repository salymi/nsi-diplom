# app.py
# -*- coding: cp1251 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Подключение к базе данных
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'ibm_db_sa://db2admin:jesus@192.168.1.99:53590/TOOLSDB?charset=cp1251'
app.secret_key = "flask rocks!"
db = SQLAlchemy(app)
manager = LoginManager(app)
