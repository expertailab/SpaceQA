# SpaceQA
This prototype shows an extractive question answering system, which extracts the correct answer to a question from a context document or paragraph. The most relevant paragraphs for a given question are retrieved using [ColBERT](https://arxiv.org/abs/2004.12832), and a [RoBERTa](https://arxiv.org/abs/1907.11692) transformer language model finetuned on [SQUAD 2.0](https://arxiv.org/abs/1806.03822) dataset is used for question answering.

The question answering module is able to answer 'WH questions' (What, When, Where, How...), however it is not designed to answer Yes/No or multi-hop questions (where the answer is obtained from multiple paragrahs), so the answers must be found explicitly in the retrieved paragraphs.

## Requirements:
* [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)

## Installation:
Create a new conda environment:
```bash
conda create -n spaceqa python=3.8
conda activate spaceqa
cd SpaceQA
pip install -r requirements.txt
```

## Execution
```bash
streamlit run run_question_answering.py -- --question_answering_endpoint=$QUESTION_ANSWERING_ENDPOINT --colbert_retriever_endpoint=$COLBERT_RETRIEVER_ENDPOINT  --elasticsearch=$ELASTICSEARCH_ENDPOINT
```

## Question Answering and Retriever Modules
### Requirements:
* Java JDK 11

Create a new conda environment:
```bash
cd question_answering/src
conda create -n colbert python=3.8
conda activate colbert
pip install -q git+https://github.com/terrierteam/pyterrier_colbert.git
pip install jsonschema
conda install -c pytorch faiss-gpu=1.6.5
```

You may need to set JAVA_HOME environment variable. Example in a Linux machine:
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/
```
You have to create a [colbertindex](https://github.com/terrierteam/pyterrier_colbert) and change [this line](./question_answering/src/colbert_retriever/colbert_retriever.py#L10) to use the created colbertindex.

To run the question answering and retriever module:
```bash
python app.py
```

By default the endpoints will be:
* http://localhost:8080/get_contexts, retriever endpoint which receives a question and returns the context to answer the question
* http://localhost:8080/answer_question, question answering endpoint which receive a question and a list of contexts, and returns the answer for each context.

## Elasticsearch Module
We have an [Elasticsearch](https://www.elastic.co/elasticsearch/) with two indices: "paragraph" and "document". These are the mappings of the paragraph index :
```json
"mappings":{"properties":{"document":{"type":"keyword"},"faiss_id":{"type":"integer"},"is_suggestion":{"type":"boolean"},"text":{"type":"text","fields":{"keyword":{"type":"keyword"}}}}
```
And the mappings of the "document" index:
```json
"mappings":{"properties":{"name":{"type":"text","fields":{"keyword":{"type":"keyword","ignore_above":256}}}}
```
Note that there must be a direct correspondence between the "faiss_id" and the vector id in the colbertindex.
