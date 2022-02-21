import streamlit as st
import SessionState
import json
import argparse
from question_answering_demo_ui import run_app


def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))


def main(args):
    # Use the full page instead of a narrow central column
    st.set_page_config(page_title="Question Answering Demo", layout="wide", page_icon="favicon.png")

    session_state = SessionState.get(isLoggedIn=False, logged_in_data=None)
       
    if session_state.isLoggedIn:
        run_app(args, session_state)
    else:
        logged_in_data = True

        if bool(logged_in_data):
            session_state.isLoggedIn = True
            session_state.valid_list = []
            #session_state.logged_in_data = format_login_data(logged_in_data)
            session_state.logged_in_data = {
            "name" : 'Test User',
            "email" : 'test@test.com',
        }
            rerun()
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Question Answering Demo',
        epilog='Copyright Expert System Iberia 2022')
    parser.add_argument(
        '--question_answering_endpoint',
        required=False,
        default='http://localhost:8080/answer_question',
        help='Question Answering module API endpoint')
    parser.add_argument(
        '--colbert_retriever_endpoint',
        required=False,
        default='http://localhost:8080/get_contexts',
        help='ColBERT retriever API endpoint')
    parser.add_argument(
        '--elasticsearch',
        required=False,
        default='http://localhost:8091',
        help='Elasticsearch API endpoint')
    args = parser.parse_args()
    main(args)
