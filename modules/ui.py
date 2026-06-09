# modules/ui.py

import streamlit as st

def render_header_footer():

    st.markdown("""
    <div class="fixed-header">
        <h1><span style="color:red;">⚖️MERIT⚖️</span></h1>
        <h2>
            <span style="color:red;">M</span>anuscript 
            <span style="color:red;">E</span>ditorial 
            <span style="color:red;">R</span>eviewer and 
            <span style="color:red;">I</span>nspection 
            <span style="color:red;">T</span>ool
        </h2>
    </div>

    <div class="fixed-footer">
        Scholarly Academic Resource by 
        <a href="https://wawerujm.github.io" target="_blank" 
        style="color:white;text-decoration:underline;">
        James Waweru
        </a>
    </div>
    """, unsafe_allow_html=True)


def hide_sidebar():
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)


def render_progress(step):

    steps = [
        "Upload",
        "Methodology",
        "Statistics",
        "Coherence",
        "Scoring",
        "Output"
    ]

    progress = step / len(steps)

    st.progress(progress)

    cols = st.columns(len(steps))

    for i, label in enumerate(steps):
        if i + 1 == step:
            cols[i].markdown(f"**🔴 {label}**")
        else:
            cols[i].markdown(label)


def navigation_buttons(current_step):

    col1, col2 = st.columns(2)

    if current_step > 1:
        if col1.button("⬅ Back"):
            st.session_state.step -= 1
            st.rerun()

    if current_step < 6:
        if col2.button("Next ➡"):
            st.session_state.step += 1
            st.rerun()