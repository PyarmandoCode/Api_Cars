from app import app,db
from .models import Autos
from flask import request
from flask_cors import CORS, cross_origin


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator        



@app.route('/')
def index():
    return {"Msj":"Bienvenido a la Pagina de Autos"}

@app.route('/autos',methods=['POST','GET'])
def handle_autos():
    if request.method=='POST':
        if request.is_json:
            data=request.get_json()
            new_auto=Autos(nombre=data['nombre'],
                           detalle=data['detalle'],
                           imagen=data['imagen'],
                           precio=data['precio']
                           )
            db.session.add(new_auto)
            db.session.commit()

            return {"message": f"Auto {new_auto.nombre} has been created successfully "}
        
        else:
            return {"error":"The request payload is not in Json format"}
        
    elif request.method =='GET':
        autos=Autos.query.filter_by(estado=True).all()#Select * From Autos
        results = [
            {
            "auto":auto.idauto,
            "nombre":auto.nombre,
            "detalle":auto.detalle,
            "precio":auto.precio,
            "imagen":auto.imagen,
            "estado":auto.estado
            } for auto in autos]
        
        return {"Count":len(autos),"Autos":results,"message":"success"}
    
@app.route('/auto/<auto_id>',methods=['GET','PUT','DELETE','OPTIONS']) 
@crossdomain(origin='*')
def handle_auto(auto_id):
    auto=Autos.query.get_or_404(auto_id)
    if request.method == 'GET':
        response = {
            "auto":auto.idauto,
            "nombre":auto.nombre,
            "detalle":auto.detalle,
            "precio":auto.precio,
            "imagen":auto.imagen,
            "estado":auto.estado
        }
        return {"message":"success","auto":response}
    
    elif request.method=='PUT':
        data = request.get_json()
        auto.nombre=data["nombre"]
        auto.detalle=data["detalle"]
        auto.precio=data["precio"]
        auto.imagen=data["imagen"]
        
        
        db.session.add(auto)
        db.session.commit()

        return {"message":f"Auto {auto.nombre} successfully updated"}
    
    elif request.method=='DELETE':
        db.session.delete(auto)
        db.session.commit()

        return {"message":f"Auto {auto.nombre} successfully deleted"}

