from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

#Paso 1.-Creando la Aplicacion

app=Flask(__name__)

#Paso 2.-Configurando la aplicacion con la BD

app.config.from_object(Config)


#Paso 3.-Conectando la Aplicacion con la BD
db=SQLAlchemy(app)

from app import models,rutas






