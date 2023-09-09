from app import db

class Autos(db.Model):
    idauto =db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String())
    detalle=db.Column(db.Text)
    imagen=db.Column(db.String())
    precio=db.Column(db.Numeric(7,2))
    estado=db.Column(db.Boolean,default=True)
    puertas=db.Column(db.Integer)
    
    
    

