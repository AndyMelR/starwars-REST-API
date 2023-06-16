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
from models import db, User, People, Planet, Favorite
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
    users = User.query.all()
    response_user = [user.serialize() for user in users]
    response_body = {
        "msg": "Users list"
    }

    return jsonify(response_user), 200 


@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.get(user_id)
    user = user.serialize()
    return jsonify(user), 200


@app.route('/people', methods = ['GET'])
def get_people():
    characters = People.query.all()
    response_people = [people.serialize() for people in characters]
    response_body = {
        "msg": "People list"
    }

    return jsonify(response_people), 200 


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_character(people_id):
    character = People.query.get(people_id)
    oneCharacter = character.serialize()
    return jsonify(oneCharacter), 200


@app.route('/planet', methods = ['GET'])
def get_planet():
    planets = Planet.query.all()
    response_planet = [planet.serialize() for planet in planets]
    response_body = {
        "msg": "Planet list"
    }

    return jsonify(response_planet), 200 


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    onePlanet = planet.serialize()
    return jsonify(onePlanet), 200


@app.route('/<int:user_id>/favorite', methods = ['GET'])
def get_user_favorites(user_id):
    favorite = Favorite.query.filter_by(user_id = user_id).all()
    favorite_user = [favorite.serialize() for favorite in favorite]

    return jsonify(favorite_user), 200


@app.route('/<int:user_id>/favorite/people/<int:people_id>', methods = ['GET'])
def post_people_to_favorite(user_id, people_id): 
    favorite = Favorite(user_id = user_id, people_id = people_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {
        "msg": "Personaje agregado a favoritos "
    }
    return jsonify(response_body), 200


@app.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods = ['GET'])
def post_planet_to_favorite(user_id, planet_id): 
    favorite = Favorite(user_id = user_id, planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {
        "msg": "Planeta agregado a favoritos "
    }
    return jsonify(response_body), 200


@app.route('/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(user_id, people_id): 
    people_deleted = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    db.session.delete(people_deleted)
    db.session.commit()
    
    response_body = {
        "msg": "Personaje borrado"
    }
    return jsonify(response_body), 200  


@app.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(user_id, planet_id): 
    planet_deleted = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    db.session.delete(planet_deleted)
    db.session.commit()
    
    response_body = {
        "msg": "Planeta borrado!"
    }
    return jsonify(response_body), 200   

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)