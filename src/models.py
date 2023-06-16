import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250))
    height = db.Column(Integer)
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.Integer)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }


class Planet(db.Model):
    __tablename__ = 'planet'

    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable = False)
    climate = Column(String(250))
    population = Column(Integer)
    diameter = Column(Integer)
    terrain = Column(String(250))
    surface_water = Column(Integer)
    orbital_period = Column(Integer)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "population": self.population,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People)
    

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }
