from flask import Flask, request
from flask_restful import Resource
from uaas_gcp import Uaas

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')

uaas_dao = Uaas()


class Uaas_cantiere(Resource):
    def post(self, idCantiere):
        idCantiere = str(idCantiere)
        cantiere = request.json
        if cantiere == "" or cantiere == None:
            return None, 400

        body, code = uaas_dao.add_cantiere(idCantiere, cantiere)
        return body, code
    
    
    def get(self, idCantiere):
        idCantiere = str(idCantiere)
        body, code = uaas_dao.get_cantiere(idCantiere)
        return body, code
        


class Uaas_umarell(Resource):
    def post(self, idUmarell):
        idUmarell = str(idUmarell)
        umarell = request.json
        if umarell == "" or umarell == None:
            return None, 400
        
        body, code = uaas_dao.add_umarell(idUmarell, umarell)
        return body, code
    
    
    def get(self, idUmarell):
        idUmarell = str(idUmarell)
        body, code = uaas_dao.get_umarell(idUmarell)
        return body, code



class Uaas_clean(Resource):
    def post(self):
        return uaas_dao.clean(), 200
    def get(self):
        return uaas_dao.clean(), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)