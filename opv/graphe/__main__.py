from flask import Flask
from opv.graphe import graphe_api
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
app.register_blueprint(graphe_api)

if __name__ == "__main__":
    app.run()