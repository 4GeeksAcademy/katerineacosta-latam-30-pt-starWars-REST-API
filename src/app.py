"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from operator import and_
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Favorite, Planet, db, User, People
import datetime
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

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.toDict() for p in people]), 200

@app.route('/people', methods=['POST'])
def post_people():
    new_person = People()
    
    new_person.name = request.json['name']
    new_person.gender = request.json['gender']
    new_person.hair_color = request.json['hair_color']
    new_person.height = request.json['height']

    db.session.add(new_person)
    db.session.commit()
    
    return jsonify({
        "message": 'person created',
        "user_id": new_person.id
    }),201

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    return jsonify(person.toDict()),200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.toDict() for p in planets]), 200

@app.route('/planets', methods=['POST'])
def post_planets():
    new_planet = Planet()

    new_planet.name = request.json['name']
    new_planet.diameter = request.json['diameter']
    new_planet.climate = request.json['climate']
    new_planet.population = request.json['population']

    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify({
        "message": 'planet created',
        "user_id": new_planet.id
    }),201

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.toDict()),200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.toDict() for u in users]), 200

@app.route('/users', methods=['POST'])
def post_user():
    new_user = User()

    new_user.email = request.json['email']
    new_user.name = request.json['name']
    new_user.lastname = request.json['lastname']
    new_user.password = request.json['password']
    new_user.subscription_date = datetime.datetime.now()

    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": 'usuario creado',
        "user_id": new_user.id
    }),201


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')

    user_favorites = Favorite.query.filter_by(user_id=user_id)
    favorites = [uf.toDict() for uf in user_favorites]
    favorites_mapped = [uf['people'] if uf['planet'] is None  else uf['planet'] for uf in favorites]
    return jsonify(favorites_mapped)


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    user_id = request.args.get('user_id')

    favorite = Favorite()

    favorite.planet_id = planet_id
    favorite.user_id = user_id

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "message": 'favorite planet created',
        "favorite_id": favorite.id
    }),201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    user_id = request.args.get('user_id')

    favorite = Favorite()
    
    favorite.people_id = people_id
    favorite.user_id = user_id

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "message": 'favorite people created',
        "favorite_id": favorite.id
    }),201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    user_id = int(request.args.get('user_id'))
    
    user_favorite = Favorite.query.filter_by(planet_id=planet_id, user_id=user_id).one()

    db.session.delete(user_favorite)
    db.session.commit()

    return jsonify({ "msg": "borrado"}), 202

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    user_id = request.args.get('user_id')
    
    user_favorite = Favorite.query.filter_by(people_id=people_id, user_id=user_id).one()

    db.session.delete(user_favorite)
    db.session.commit()
    return jsonify({ "msg": "borrado"}), 202


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
