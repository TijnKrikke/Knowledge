import streamlit as st
from solver import Solver
from parser import load_kb
import os

main, panel = st.columns([3, 1])

with main:
    st.set_page_config(
        page_title="Main",
        layout="wide"
    )

    @st.cache_data
    def load_kb_cached():
        games_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "games.yml"))
        questions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "questions.yml"))
        rules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "rules.yml"))
        return load_kb(games_path, questions_path, rules_path)

    kb = load_kb_cached()


    if "solver" not in st.session_state:
        st.session_state.solver = Solver(kb=kb, debug=True)

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
            # We simulate a solver to find the number of remaining games if this answer is chosen
            simulated_solver = Solver(kb=kb)
            simulated_solver.facts = st.session_state.solver.facts.__class__(
                fact_pos=st.session_state.solver.facts.fact_pos.copy(),
                fact_neg=st.session_state.solver.facts.fact_neg.copy(),
                fact_idc=st.session_state.solver.facts.fact_idc.copy(),
                fact_known=st.session_state.solver.facts.fact_known.copy(),
                remaining_rules=st.session_state.solver.facts.remaining_rules.copy(),
                remaining_games=st.session_state.solver.facts.remaining_games.copy()
            )
            simulated_solver.process_answer(answer)
            nr_games = len(simulated_solver.get_games_left())
            st.button(answer.text, on_click=st.session_state.solver.process_answer, args=(answer,), help=f"Remaining: {nr_games}")            

with panel:
    st.subheader("Aspects Known")
    aspects_pos, aspects_neg = st.session_state.solver.get_aspects()

    if not aspects_pos and not aspects_neg:
        st.markdown("This bar will show the known aspects as you answer questions.")
    else:
        st.markdown("Here are some aspects that have been determined so far:")
        for aspect in aspects_pos:
            st.success(f"- {aspect.name}")
        for aspect in aspects_neg:
            st.error(f"- {aspect.name}")
