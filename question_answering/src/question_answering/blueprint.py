from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from question_answering.question_answering import QuestionAnswering

blueprint = Blueprint('question_answering', __name__)

@blueprint.record_once
def record(setup_state):
    blueprint.question_answering = QuestionAnswering()
    print("QuestionAnswering loaded!")
    print(blueprint.question_answering.nlp)

@blueprint.route('/answer_question', methods=['POST'])
def answer_question():
    try:
        json = request.get_json(force=True)
        validate(json, {
            'type': 'object',
            'required': ['question','contexts'],
            'properties': {
                'question': { 'type': 'string' },
                'contexts': { 'type': 'array', 'items': { 'type': 'string' }}
            }
        })

        results = blueprint.question_answering.answer_question(json['question'], json['contexts'])
        return jsonify({"answers":results})

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500
