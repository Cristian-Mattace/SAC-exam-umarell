from flask import Flask, render_template, request, jsonify
from flask_restful import Api
from wtforms import Form, SubmitField, validators, StringField, BooleanField
from uaas_gcp import Uaas
from api import Uaas_cantiere, Uaas_umarell, Uaas_clean


app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')

class uaasFORM(Form):
    cap =   StringField('Cap', [validators.InputRequired()])
    umarell = BooleanField('Umarell')
    cantiere = BooleanField('Cantiere')
    Submit  =   SubmitField('Submit')


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

api = Api(app)

basePath = '/api/v1'

uaas_dao = Uaas()


api.add_resource(Uaas_cantiere, f'{basePath}/cantiere/<int:idCantiere>')
api.add_resource(Uaas_umarell, f'{basePath}/umarell/<int:idUmarell>') 
api.add_resource(Uaas_clean, f'{basePath}/clean') 


@app.route('/search', methods=['GET', 'POST'])
def index():
    form = uaasFORM(request.form)

    if request.method == 'POST':
        
        if form.umarell.data == True:
            umarells = uaas_dao.get_umarell_by_cap(form.cap.data)
        else:
            umarells = ""
        
        if form.cantiere.data == True:
            cantieri = uaas_dao.get_cantieri_by_cap(form.cap.data)
        else:
            cantieri = ""
        
        return render_template("index.html", 
                           form = form,
                           umarells = umarells,
                           cantieri = cantieri), 200        

    form = uaasFORM(obj=Struct(**{"Cap": ""}))
    return render_template("index.html", 
                           form = form,
                           umarells = "",
                           cantieri = ""), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
