from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    favourite_people = db.relationship('Favourite_People', backref="user")
    favourite_planet = db.relationship('Favourite_Planet', backref="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favourite_people": [fav.serialize() for fav in self.favourite_people],
            "favourite_planet": [fav.serialize() for fav in self.favourite_planet],
            # do not serialize the password, its a security breach
        }


# PEOPLE & FAVOURITE PEOPLE
class People(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    favourite_people = db.relationship('Favourite_People', backref="people")
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            }
    
class Favourite_People(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))

    def __repr__(self):
        return '<Favourite_People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            }


# PLANETS & FAVOURITE PLANETS
class Planets(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    favourite_planet = db.relationship('Favourite_Planet', backref="planets")


    def __repr__(self):    
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            }

class Favourite_Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.id))

    def __repr__(self):    
        return '<Favourite_Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            }

