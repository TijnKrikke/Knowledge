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
    st.session_state.solver = Solver(games=kb.games)


question = st.session_state.solver.get_question(kb.questions)
matches = st.session_state.solver.get_games_left()

if question is None:
    st.subheader("Recommendation")
    matches = st.session_state.solver.get_games_left()
    if matches:
        for g in matches:
            st.markdown(f"- **{g.name}** — {g.description}")
        st.success(f"Top recommendation: {matches[0].name}")
    else:
        st.info("No recommendation.")
else:
    st.markdown(f"**Games left:** {len(matches)}")
    st.subheader("Question")
    st.markdown(question.text)
    for answer in question.options:
        st.button(answer.text, on_click=st.session_state.solver.process_answer, args=(answer,))



