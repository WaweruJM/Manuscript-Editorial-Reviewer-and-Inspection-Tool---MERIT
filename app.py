import streamlit as st
import os


st.set_page_config(
    page_title="MERIT | Manuscript Editorial Review and Inspection Tool",
    page_icon="🔎",
    layout="wide",

)

# Load custom CSS
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Fixed header and footer
st.markdown("""
<div class="fixed-header">
    <h1>⚖️ <span class="merit-title">MERIT</span> ⚖️</h1>
    <h2>
        <span class="merit-letter">M</span>anuscript 
        <span class="merit-letter">E</span>ditorial 
        <span class="merit-letter">R</span>eview and 
        <span class="merit-letter">I</span>nspection 
        <span class="merit-letter">T</span>ool
    </h2>
</div>
<div class="fixed-footer">
    Scholarly Academic Resource by 
    <a href="https://wawerujm.github.io" target="_blank" style="color:white;text-decoration:underline;">
    James Waweru
    </a>
</div>
""", unsafe_allow_html=True)

# Content wrapper
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = 1
if "df" not in st.session_state:
    st.session_state.df = None
if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "filename" not in st.session_state:
    st.session_state.filename = None
if "column_categories" not in st.session_state:
    st.session_state.column_categories = {}
if "cleaning_log" not in st.session_state:
    st.session_state.cleaning_log = []
if "test_results" not in st.session_state:
    st.session_state.test_results = []

# Routing based on page number
if st.session_state.page == 1:
    import pages.page1_upload as page1
    page1.show()
elif st.session_state.page == 2:
    import pages.page2_preview as page2
    page2.show()
elif st.session_state.page == 3:
    import pages.PAGE3_Methodology_Review as page3
    page3.show()
elif st.session_state.page == 4:
    import pages.PAGE4_Statistical_Analysis_Review as page4
    page4.show()
elif st.session_state.page == 5:
    import pages.PAGE5_Reporting_of_Results_Review as page5
    page5.show()
elif st.session_state.page == 6:
    import pages.PAGE6_Summary_and_Downloadable_Report as page6
    page6.show()

else:
    st.error("Invalid page. Redirecting to start.")
    st.session_state.page = 1
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)