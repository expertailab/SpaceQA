from flask import Flask

from internal.blueprint import blueprint as InternalBlueprint
from question_answering.blueprint import blueprint as QuestionAnsweringBlueprint
from colbert_retriever.blueprint import blueprint as ColbertBlueprint

app = Flask(__name__)

app.register_blueprint(InternalBlueprint)
app.register_blueprint(QuestionAnsweringBlueprint)
app.register_blueprint(ColbertBlueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
