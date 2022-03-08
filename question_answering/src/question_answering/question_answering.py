from transformers import pipeline

class QuestionAnswering(object):

    def __init__(self):
        model_name = "a-ware/roberta-large-squadv2"
        #self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name, device=0)

    def answer_question(self, question, contexts):
        results = []
        for context in contexts:
            try:
                QA_input = {
                'question': question ,
                'context': context
                }
                res = self.nlp(QA_input)
                data= {'context':context,'answer': res['answer'], 'score':res['score'], 'start':res['start'], 'end':res['end']}
                results.append(data)
            except:
                continue
        return results
