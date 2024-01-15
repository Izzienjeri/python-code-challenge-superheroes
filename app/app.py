#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the SuperHeroes RESTful Api"
        }

        response = make_response(response_dict, 200)

        return response
api.add_resource(Home, '/')

class Heroes(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Hero.query.all()]

        response = make_response(jsonify(response_dict_list, 200))
        return response
api.add_resource(Heroes, '/heroes')

class OneHero(Resource):
    def get(self, id):
       hero = Hero.query.filter(Hero.id == id).first()

       if hero:
           response_dict = hero.to_dict()
           response = make_response(jsonify(response_dict), 200) 
           return response
       else:
           response_dict2 = {
               "error": "Hero not found"
           }
           response2 = make_response(jsonify(response_dict2), 404)
           return response2
       
api.add_resource(OneHero, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        response_dict_list = [power.to_dict() for power in Power.query.all()]

        response = make_response(jsonify(response_dict_list), 200)
        return response
api.add_resource(Powers, '/powers')

class OnePower(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()

        if power:
            response_dict = power.to_dict()
            response = make_response(jsonify(response_dict), 200)
            return response
        else:
            response_dict2 = {
                "error": "Power not found"
            }
            response2 = make_response(jsonify(response_dict2), 404)
            return response2
        
    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()

        if power:
            for attr in request.form:
                setattr(power, attr, request.form.get(attr))

            db.session.add(power)
            db.session.commit()

            response_dict = power.to_dict()
            response = make_response(jsonify(response_dict), 200)

            return response
        else:
            response_dict2 = {
                "error": "Power not found"
            }
            response2 = make_response(jsonify(response_dict2, 404))
            return response2
        
api.add_resource(OnePower, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):

        strength = request.form["strength"]
        power_id = request.form["power_id"]
        hero_id = request.form["hero_id"]

        if strength and power_id and hero_id:
            new_heropower = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)

            db.session.add(new_heropower)
            db.session.commit()

            new_heropower_dict = new_heropower.to_dict()

            response = make_response(jsonify(new_heropower_dict), 201)
            return response
        
        else:
            response_dict2 = {
                "errors": ["Validation errors"]
    
            }

            response = make_response(jsonify(response_dict2), 404)
    
api.add_resource(HeroPowers, '/hero_powers')

    
        

if __name__ == '__main__':
    app.run(port=5555)