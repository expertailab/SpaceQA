import streamlit as st
import argparse
import requests
import json
import hydra
from passage_retriever import main as pr_main
from elasticsearch import Elasticsearch
import random

if not hydra.core.global_hydra.GlobalHydra.instance().is_initialized():
    hydra.initialize()
cfg = hydra.compose("conf/dense_retriever.yaml")
cfg.conf.retrieval = 'colbert'

@st.cache
def get_document_name(id):
    res = es.get(index="document", id=id)
    return res['_source']['name']

@st.cache
def get_documents():
    res = es.search(index="document", size = 10000) 
    return [elem['_source']['name'] for elem in res['hits']['hits']]

@st.cache
def suggest_paragaphs():
    res = es.search(index="paragraph",q="is_suggestion:true",_source_includes =["text", "document"])
    suggestions = [ (item['_source']['text'],get_document_name(item['_source']['document'])) for item in res['hits']['hits']]
    return suggestions

@st.cache
def answer_question(question, args, filter_document):
    cfg.conf.question = question
    cfg.conf.colbert_retriever_endpoint = args.colbert_retriever_endpoint
    cfg.conf.elasticsearch = args.elasticsearch
    result = pr_main(cfg.conf)

    filtered_contexts = list(filter(lambda k: len(k)>73 , result['text'].tolist()))

    body = {"question":cfg.conf.question, "contexts":filtered_contexts}

    res = requests.post(args.question_answering_endpoint, json=body)

    if res.status_code != 200:
        raise RuntimeError("Something went wrong while calling the question answering module, try again later")

    response_json = res.json()

    for elem in response_json['answers']:
        elem['document'] = get_document_name(result.iloc[result.index[result['text']==elem['context']][0]]['document'])

    filtered_response = list(filter(lambda k: k['score']>=0.5 and (len( k['answer'])>1 or k['answer'].isalnum()), response_json['answers']))

    if(filter_document != ""):
        filtered_response = list(filter(lambda k: k['document']==filter_document, filtered_response))

    return sorted(filtered_response, key=lambda k: k['score'], reverse=True),sorted(response_json['answers'], key=lambda k: k['score'], reverse=True) 

def print_answer(answer):
    st.write("**Answer:** " + answer['answer'])
    st.write("**Context:** " + answer['context'][:answer['start']]+
        "**<span style='color:rgb(255, 255, 255);background-color:rgba(0, 120, 0, 1)'>"+answer['context'][answer['start']:answer['end']]+'</span>**'+
        answer['context'][answer['end']:], unsafe_allow_html=True)
    st.write("**Document:** %s" % (answer['document']))
    st.write("**Score:** " + str(round(answer['score'],2)))

def run_answerquestion(args, doc, filter_document):
    sorted_answers, all_answers = answer_question(doc,args,filter_document) 

    if (len(sorted_answers) == 0):
        if (len(all_answers) > 0):
            st.write("**I am not sure about the answer, do you want to see possible answers?**")
            with st.expander("Show answers"):
                for all_answer in all_answers[0:3]:
                    print_answer(all_answer)
        else:
            st.write("**There is no answer for that question**")
    else:
        print_answer(sorted_answers[0])
        if (len(sorted_answers) > 1):
            with st.expander("Other possible answers"):
                for sorted_answer in sorted_answers[1:3]:
                    print_answer(sorted_answer)

def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def print_title(title):
     st.markdown("""
        <img style="float: right; width: 200px;" src="https://esatde.expertcustomers.ai/images/EAI PRIMARY TRANSPARENT.png">
        <img style="float: right; width: 200px;" src="https://esatde.expertcustomers.ai/images/ESA_logo_2020_Deep-1024x643.jpg">
        <h1 style="position: relative">"""+title+"""</h1>
        """, unsafe_allow_html=True)

def question_answering_demo(args):
    title = "SpaceQA"
    print_title(title)
    questions = ["", "What is Athena's orbit?",
    "When is MarsFAST scheduled to be launched?",
    "When is MarsFAST expected to arrive?", "What is the aim of MarsFast?","How much does the MarsFAST rover weigh?","What is SPICA?","How far is the moon from the Earth?"]

    if st.button('Click to open demo video'):
        video_file = open('./video.webm', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    option = st.selectbox(
    "Choose a question below:",
     questions)

    documents = [""] + get_documents()

    filter_document = st.selectbox(
    "Filter by document (optional, but recommended):",
     documents)

    if option or filter_document:
        run_answerquestion(args, option, filter_document)

    st.text("")

    doc = st.text_area('You can also write or modify your own question here:', option)

    if st.button('Give me an answer'):
        run_answerquestion(args, doc, filter_document)

    st.text("")
    st.write("""
    If you need inspiration , please click on 'Give me a prompt'.
    """)

    if st.button('Give me a prompt'):
        suggestions = suggest_paragaphs()
        random_paragraph = random.choice(suggestions)
        st.write("""
        **Prompt:** %s...
        """ % random_paragraph[0].replace("1.1 Background ",'')[:300])

def about():
    print_title("About")
    st.write("""
    ### SpaceQA
    This prototype shows an extractive question answering system, which extracts the correct answer to a question from a context document or paragraph. The most relevant paragraphs for a given question are retrieved using [ColBERT](https://arxiv.org/abs/2004.12832), and a [RoBERTa](https://arxiv.org/abs/1907.11692) transformer language model finetuned on [SQUAD 2.0](https://arxiv.org/abs/1806.03822) dataset is used for question answering.

    The question answering module is able to answer 'WH questions' (What, When, Where, How...), however it is not designed to answer Yes/No or multi-hop questions (where the answer is obtained from multiple paragrahs), so the answers must be found explicitly in the retrieved paragraphs.

    If you have any doubt or suggestion, please send it to [Cristian](mailto:cberrio@expert.ai), [Andrés](mailto:agarcia@expert.ai) or [Jose](mailto:jmgomez@expert.ai).
    """)

def run_app(args, session_state=None):
    global es
    es = Elasticsearch(args.elasticsearch,verify_certs=False)
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    menu_opts = {
        1: "SpaceQA",
        2: "About"
    }

    menu_box = st.sidebar.selectbox('MENU', (
        menu_opts[1],
        menu_opts[2]
    ))

    if menu_box == menu_opts[1]:
        question_answering_demo(args)

    if menu_box == menu_opts[2]:
        about()
