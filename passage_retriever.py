from elasticsearch import Elasticsearch

from omegaconf import DictConfig, OmegaConf
import logging

import pandas as pd
import requests
import json

with open('./mission_to_code.json') as f:
  mission_to_code = json.load(f)

logger = logging.getLogger()
    
def colbertRetriever(cfg: DictConfig):
	question = cfg.question
	colbert_endpoint = cfg.colbert_retriever_endpoint
	
	data = {"question":question}
	res = requests.post(colbert_endpoint, json=data)
	
	if res.status_code != 200:
		raise RuntimeError("Something went wrong while calling the ColBERT retriever module, try again later")
	
	doc_ids = res.json()['contexts']
	question_lower = question.lower()
	dataframe = pd.DataFrame(columns=['id','text','document'])

	for doc_id in doc_ids:
		es_doc = getDocumentFromFaissId(doc_id)
		for mission in mission_to_code.keys(): ## Heuristic: if mission in question, filter if context does not belong to the mission documents
			if mission in question_lower and mission_to_code[mission] != es_doc['_source']['document']: 
				break
		else:
			my_id = es_doc['_id']
			text = es_doc['_source']['text'] 
			doc = es_doc['_source']['document']
			data = {"id": my_id,"text": text, "document": doc}
			dataframe = dataframe.append(data, ignore_index=True)
			continue
		break
		

	return dataframe

def getDocumentFromFaissId(faiss_id):
	es_body = {
		"query":{"term":{"faiss_id": faiss_id}},
		"_source":["text","document"]
	}
	res = es.search(index="paragraph", body=es_body)

	return res['hits']['hits'][0]

def main(cfg: DictConfig):
	global es
	es = Elasticsearch(cfg.elasticsearch,verify_certs=False)
	question = cfg.question
	retrieval = cfg.retrieval

	result = None
	if (retrieval=="colbert"):
		result = colbertRetriever(cfg)

	return result

if __name__ == "__main__":
	main()
