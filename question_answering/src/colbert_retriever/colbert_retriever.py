import pyterrier as pt
pt.init()
import pyterrier_colbert.indexing
import pyterrier_colbert
checkpoint="http://www.dcs.gla.ac.uk/~craigm/colbert.dnn.zip"

class Colbert(object):

    def __init__(self):
        pyterrier_colbert_factory = pyterrier_colbert.ranking.ColBERTFactory(checkpoint, "/home/test/ESA-TDE/colbert", "colbertindex",gpu=False)
        #pyterrier_colbert_factory = pyterrier_colbert.ranking.ColBERTFactory(checkpoint, "/home/test/ESA-TDE/colbert", "colbertindex",gpu=True)
        pyterrier_colbert_factory_qa = pyterrier_colbert.ranking.ColBERTFactory(checkpoint, "/home/test/ESA-TDE/colbert", "qa-colbertindex",gpu=False)
        #pyterrier_colbert_factory_qa = pyterrier_colbert.ranking.ColBERTFactory(checkpoint, "/home/test/ESA-TDE/colbert", "qa-colbertindex",gpu=True)
        self.colbert_e2e = {"CDF":pyterrier_colbert_factory.end_to_end(),"QA":pyterrier_colbert_factory_qa.end_to_end()}

    def get_contexts(self, question, index = "CDF"):
        results = (self.colbert_e2e[index] % 10).search(question)
        return [int(doc_id)-1 for doc_id,score in zip(results['docno'].tolist(),results['score'].tolist()) if score>=19]
