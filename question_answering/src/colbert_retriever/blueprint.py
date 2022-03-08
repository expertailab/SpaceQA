from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from colbert_retriever.colbert_retriever import Colbert

blueprint = Blueprint('colbert', __name__)

@blueprint.record_once
def record(setup_state):
    blueprint.colbert = Colbert()
    print("Colbert loaded!")
    print(blueprint.colbert)

@blueprint.route('/get_contexts', methods=['POST'])
def get_contexts():
    try:
        json = request.get_json(force=True)
        validate(json, {
            'type': 'object',
            'required': ['question'],
            'properties': {
                'question': { 'type': 'string' },
		'index': { 'type': 'string' }
            }
        })

        results = blueprint.colbert.get_contexts(json['question']) if not 'index' in json else blueprint.colbert.get_contexts(json['question'],json['index'])
        return jsonify({"contexts":results})

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500
