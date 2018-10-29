from flask import Flask
from opv.graphe import graphe_api
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(graphe_api)

if __name__ == "__main__":
    app.run()