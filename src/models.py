from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    subscription_date = db.Column(db.Date(), nullable=False)

    def __repr__(self):
        return "Objeto User "+ self.name
    
    def toDict(self):
       return { "id":self.id, "name":self.name,  "lastname":self.lastname, "email":self.email }
    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False )
    hair_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    def toDict(self):
       return { "id":self.id, "name":self.name,  "height":self.height, "hair_color":self.hair_color, "gender":self.gender }

class Planet(db.Model):
    __tablename__= 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    climate =  db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)

    def toDict(self):
       return { "id":self.id, "name":self.name,  "diameter":self.diameter, "climate":self.climate, "population":self.population }

class Favorite(db.Model):
    __tablename__= 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    def toDict(self):
       return { "id":self.id, "people_id":self.people_id,  
               "people": None if self.people is None else  self.people.toDict(), 
               "planet_id":self.planet_id, 
               "planet": None if self.planet is None else  self.planet.toDict(),
               "user_id": self.user_id
                }


