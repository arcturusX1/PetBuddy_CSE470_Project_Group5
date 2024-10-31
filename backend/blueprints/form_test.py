from flask import Blueprint
from flask_restful import Api, Resource
from model.database import FormTestClass, db
from .forms import FormTestForm
from sqlalchemy.exc import IntegrityError

form_test_bp = Blueprint('form_test_bp', __name__)
form_test_ap = Api(form_test_bp)

class FormTestResource(Resource):
    def post(self):
        form = FormTestForm(meta={'csrf': False})

        if form.validate_on_submit():
            try:
                data = FormTestClass(
                    data_text = form.data_text.data,
                    data_bool = form.data_bool.data,
                    data_int = form.data_int.data
                )
                db.session.add(data)
                db.session.commit()
                return data.to_dict(), 201

            except IntegrityError:
                db.session.rollback()
            except Exception as e:
                db.session.rollback()
                return {'message': str(e),}, 500
        return {'message': 'Validation failed', 'errors': form.errors}, 400

form_test_ap.add_resource(FormTestResource, '/')