import streamlit as st
from solver import Solver
from parser import load_kb
import os

st.set_page_config(
    page_title="Main"
)


@st.cache_data
def load_kb_cached():
    kb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "kb.yml"))
    return load_kb(kb_path)

kb = load_kb_cached()


if "solver" not in st.session_state:
    st.session_state.solver = Solver()


question = st.session_state.solver.get_question(kb.questions) # question needs options, text 
st.subheader(f"Question")
st.markdown(question.text)


for answer in question.options:
    st.button(answer.text, on_click=st.session_state.solver.process_answer, args=(answer,))



