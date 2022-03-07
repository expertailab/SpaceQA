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
