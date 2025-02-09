"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favourite_People, Favourite_Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#  PEOPLE

@app.route('/people', methods=['GET'])
def get_people():

    get_all_people = People.query.all()

    get_people_list = list(map(lambda x: x.serialize(), get_all_people))

    return jsonify(get_people_list), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    single_person = People.query.get(people_id)

    return jsonify(single_person), 200


# PLANETS

@app.route('/planets', methods=['GET'])
def get_planets():

    get_planets = Planets.query.all()

    get_planets_list = list(map(lambda x: x.serialize(), get_planets))

    return jsonify(get_planets_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    single_planet = Planets.query.get(planet_id)

    return jsonify(single_planet), 200



# FAVOURITES

# GET USERS FAVOURITES
@app.route('/users/favourites', methods=['GET'])
def handle_users_favourites():
    request_body = request.get_json()

    user = User.query.filter_by(id = request_body["user_id"]).first()
    if not user:
        return jsonify({"ERROR": "User not found"}), 404
    return jsonify({"favourite_people": [fav.serialize() for fav in user.favourite_people],
                    "favourite_planet": [fav.serialize() for fav in user.favourite_planet]})


# POST & DELETE METHODS PEOPLE FAVOURITES

@app.route('/favorite/people/<int:id>', methods=['POST', 'DELETE'])
def handle_favourite_people(id):
    request_body = request.get_json()
    existing_favourite_character = Favourite_People.query.filter_by(user_id = request_body["user_id"], people_id = id).first()

    if request.method == 'POST':
        if existing_favourite_character:
            return jsonify({"msg": "Favourite character already exists"}), 404
        
        new_favourite_people = Favourite_People(user_id = request_body["user_id"], people_id = id)
        db.session.add(new_favourite_people)
        db.session.commit()
        return jsonify({"msg": "New favourite people added successfully", "new_favourite_people": new_favourite_people.serialize()}), 200
    
    if request.method == 'DELETE':
        if existing_favourite_character is None:
            return jsonify({"msg": "Favourite character does not exist"}), 400

        db.session.delete(existing_favourite_character)
        db.session.commit()
        return jsonify({"msg": "Favourite character deleted succesfully"}), 200



# POST & DELETE METHODS PLANETS FAVOURITES

@app.route('/favorite/planet/<int:id>', methods=['POST', 'DELETE'])
def handle_favourite_planet(id):
    request_body = request.get_json()
    existing_favourite_planet = Favourite_Planet.query.filter_by(user_id = request_body["user_id"], planet_id = id).first()

    if request.method == 'POST':
        if existing_favourite_planet:
            return jsonify({"msg": "Favourite planet already exists"}), 404
        
        new_favourite_planet = Favourite_Planet(user_id = request_body["user_id"], planet_id = id)
        db.session.add(new_favourite_planet)
        db.session.commit()
        return jsonify({"msg": "New favourite planet added successfully", "new_favourite_planet": new_favourite_planet.serialize()}), 200
    
    if request.method == 'DELETE':
        if existing_favourite_planet is None:
            return jsonify({"msg": "Favourite planet does not exist"}), 400

        db.session.delete(existing_favourite_planet)
        db.session.commit()
        return jsonify({"msg": "Favourite planet deleted succesfully"}), 200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
