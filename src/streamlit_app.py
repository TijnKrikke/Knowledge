import streamlit as st
from solver import Solver
from parser import load_kb
import os

st.set_page_config(
    page_title="Main"
)


@st.cache_data
def load_kb_cached():
    games_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "games.yml"))
    questions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "questions.yml"))
    rules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "rules.yml"))
    return load_kb(games_path, questions_path, rules_path)

kb = load_kb_cached()


if "solver" not in st.session_state:
    st.session_state.solver = Solver(kb=kb)

matches = st.session_state.solver.get_games_left()
question = st.session_state.solver.get_question()

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
    st.markdown(f"Goal: {st.session_state.solver.cur_goal_aspect}")
    st.markdown(f"Sub Goal: {st.session_state.solver.cur_sub_goal}")
    st.subheader("Question")
    st.markdown(question.text)
    for answer in question.options:
        st.button(answer.text, on_click=st.session_state.solver.process_answer, args=(answer,))



