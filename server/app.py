from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)   # <-- make sure this line exists!
CORS(app)

@app.route('/')
def home():
    return {'message': 'Welcome to the Plant Store API'}

@app.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants])

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get_or_404(id)
    return plant.to_dict()

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data['name'],
        image=data['image'],
        price=data['price'],
        is_in_stock=data.get('is_in_stock', True)
    )
    db.session.add(new_plant)
    db.session.commit()
    return new_plant.to_dict(), 201

@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    data = request.get_json()
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]
    db.session.commit()
    return plant.to_dict(), 200

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)
    db.session.commit()
    return '', 204
