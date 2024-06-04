# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Pet

#sets up Flask
app = Flask(__name__)
#connects to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#uses less ram bc doesnt track live edits
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#When set to True, the JSON responses are compact (without unnecessary spaces and indentation)
#When set to False, the JSON responses are pretty-printed with indentation and spacing for better readability
app.json.compact = False

#creates a migrate instance of the migrate class
#connects the app to the database - both parties in a migration
migrate = Migrate(app, db)
#initializes the db instance with the flask app
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)

#uses to_dict() to replace building out the whole skeleton for dictionary, for example:
# pet_dict = {'id': pet.id,
#                 'name': pet.name,
#                 'species': pet.species
#                 }
#to_dict() comes from SerializeMixIn in models.py
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = pet.to_dict()
        status = 200
    else:
        body = {'message': f'Pet {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []  # array to store a dictionary for each pet
    for pet in Pet.query.filter_by(species=species).all():
        pets.append(pet.to_dict())
    body = {'count': len(pets),
            'pets': pets
            }
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
