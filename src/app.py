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


@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()
    response_user = [user.serialize() for user in users]
    response_body = {
        "msg": "Users list"
    }

    return jsonify(response_user), 200 


@app.route('/users/<int:user_id>', methods=['GET'])
def get_specific_user(user_id):
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
def get_specific_character(people_id):
    character = People.query.get(people_id)
    singleCharacter = character.serialize()
    return jsonify(singleCharacter), 200


@app.route('/planets', methods = ['GET'])
def get_planet():
    planets = Planet.query.all()
    planet = [planet.serialize() for planet in planets]
    response_body = {
        "msg": "Planet list"
    }

    return jsonify(planet), 200 


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_specific_planet(planet_id):
    planet = Planet.query.get(planet_id)
    singlePlanet = planet.serialize()
    return jsonify(singlePlanet), 200


@app.route('/<int:user_id>/favorites', methods = ['GET'])
def get_user_favorites(user_id):
    favorite = Favorite.query.filter_by(user_id = user_id).all()
    favorite_user = [favorite.serialize() for favorite in favorite]

    return jsonify(favorite_user), 200




@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorite planet added to user"
    }
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {
        "msg": "Favorite people added to user"
    }
    return jsonify(response_body), 200


@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        response_body = {
            "msg": "Favorite planet deleted"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "Favorite planet not found"
        }
        return jsonify(response_body), 404

@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        response_body = {
            "msg": "Favorite people deleted"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "Favorite people not found"
        }
        return jsonify(response_body), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)