from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from model.database import Vet

# Fix 1: __name__ instead of name
api_test_bp = Blueprint('api_test_bp', __name__)
api_test_ax = Api(api_test_bp)

class VetListResources(Resource):
    def get(self):
        vets = Vet.query.all()
        
        # Fix 2: Convert SQLAlchemy objects to list of dictionaries
        vets_data = [{
            'id': vet.id,
            'workplace': vet.workplace
        } for vet in vets]
        
        return jsonify(vets_data)  # Return the list of vet dictionaries

api_test_ax.add_resource(VetListResources, '/api_test')