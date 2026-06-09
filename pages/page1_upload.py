# page1_upload.py
import streamlit as st
import time
from modules.parser import extract_text

def init_session():
    """Ensure all required session variables exist."""
    defaults = {
        "raw_text": "",
        "filename": "",
        "file_uploaded": False,
        "page": 1,
        "selected_guidelines": [],
        "methodology_report": None,
        "statistics_report": None,
        "results_report": None,
        "comprehensive_report": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def show():
    init_session()

    # ----------------------------- #
    # PAGE TITLE
    # ----------------------------- #
    st.markdown(
        "<h2 style='text-align:center;'>📚 MERIT - Manuscript Editorial Review & Intelligence Tool</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; font-size:16px;'>"
        "Advanced AI-powered validation of research methodology, statistical coherence, "
        "and reporting standards for scientific manuscripts."
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ----------------------------- #
    # WORKFLOW BANNER - Enhanced
    # ----------------------------- #
    st.markdown("### 🧭 Editorial Review Pipeline")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**1️⃣ Upload**")
        st.caption("DOCX or PDF")

    with col2:
        st.markdown("**2️⃣ Preview**")
        st.caption("Structural analysis")

    with col3:
        st.markdown("**3️⃣ Deep Review**")
        st.caption("Methodology • Stats • Results")

    with col4:
        st.markdown("**4️⃣ Report**")
        st.caption("Comprehensive output")

    st.markdown("---")

    # ----------------------------- #
    # UPLOAD SECTION
    # ----------------------------- #
    st.markdown("### 📁 Upload Manuscript")

    st.info("📌 **Recommended:** Microsoft Word (.docx) for complete structural analysis and section detection")

    uploaded = st.file_uploader(
        "Drag and drop or browse to upload",
        type=["docx", "pdf"],
        key="file_uploader",
        help="Accepted formats: .docx, .pdf"
    )

    # ----------------------------- #
    # FILE PROCESSING
    # ----------------------------- #
    if uploaded is not None:
        file_type = "DOCX" if uploaded.name.endswith(".docx") else "PDF"
        
        if file_type == "DOCX":
            st.success("✅ **Optimal format detected** – Full structural parsing and section extraction enabled")
        else:
            st.warning("⚠️ **PDF detected** – Structural elements (tables, sections) may have limited extraction. For best results, use DOCX format.")

        with st.spinner("🔍 Parsing manuscript and extracting content... ⏳"):
            time.sleep(1.5)  # Brief delay for UX

            try:
                text = extract_text(uploaded)

                if not text or len(text.strip()) < 500:
                    st.warning("⚠️ Document appears too short or contains minimal text. Please upload a complete manuscript.")
                    return

                # Store in session
                st.session_state.raw_text = text
                st.session_state.filename = uploaded.name
                st.session_state.file_uploaded = True

                st.success("✅ Manuscript successfully uploaded and parsed!")

                with st.expander("🔍 Preview extracted text (first 2000 characters)"):
                    st.text(text[:2000] + ("..." if len(text) > 2000 else ""))

                # Optional: Document metadata
                word_count = len(text.split())
                st.caption(f"📊 Estimated word count: {word_count:,} words")

                if st.button("➡️ **Proceed to Manuscript Preview & Review Setup**", type="primary", use_container_width=True):
                    st.session_state.page = 2
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.info("Please ensure the file is not corrupted and try again.")

    # ----------------------------- #
    # FOOTER
    # ----------------------------- #
    st.markdown("---")
    st.caption("📝 MERIT v2.0 – Editorial Intelligence System")
    st.caption("🔒 All data is processed locally and cleared after session termination")