from flask import Flask

def create_app():
    
    #Crear app de flask
    app = Flask(__name__)

    @app.route('/')
    def hola():
        return 'Hola BLOG-POST'

    return app