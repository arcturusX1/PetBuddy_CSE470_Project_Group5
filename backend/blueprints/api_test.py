from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from model.database import Vet

api_test_bp = Blueprint('api_test_bp', __name__)
api_test_ax = Api(api_test_bp)

class VetListResources(Resource):
    def get(self):
        try:
            print("Fetching vets from database...")  # Debug print
            vets = Vet.query.all()
            print(f"Found {len(vets)} vets")  # Debug print
           
            vets_data = [{
                'id': vet.id,
                'first_name': vet.first_name,
                'last_name': vet.last_name,
                'workplace': vet.workplace
            } for vet in vets]
           
            print("Returning vets data:", vets_data)  # Debug print
            return vets_data
           
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # Debug print
            return {'error': str(e)}, 500

api_test_ax.add_resource(VetListResources, '/')