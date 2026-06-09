# page2_preview.py
import streamlit as st
import re
from datetime import datetime

def init_session():
    defaults = {
        "raw_text": "",
        "filename": "",
        "file_uploaded": False,
        "selected_guidelines": [],
        "page": 1,
        "methodology_report": None,
        "statistics_report": None,
        "results_report": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def detect_study_design(text):
    """Detect study design with confidence level"""
    patterns = {
        "Randomized Controlled Trial (RCT)": {
            "pattern": r"randomi[sz]ed controlled trial|randomi[sz]ed clinical trial|RCT",
            "confidence": 0.9
        },
        "Cohort Study": {
            "pattern": r"cohort study|prospective cohort|retrospective cohort|longitudinal cohort",
            "confidence": 0.85
        },
        "Case-Control Study": {
            "pattern": r"case[- ]control|case[- ]control study|matched case",
            "confidence": 0.85
        },
        "Cross-Sectional Study": {
            "pattern": r"cross[- ]sectional|prevalence study",
            "confidence": 0.8
        },
        "Systematic Review": {
            "pattern": r"systematic review|meta[- ]analysis",
            "confidence": 0.9
        },
        "Quasi-Experimental": {
            "pattern": r"quasi[- ]experimental|non[- ]randomized",
            "confidence": 0.75
        },
        "Qualitative Study": {
            "pattern": r"qualitative|phenomenology|grounded theory|ethnography",
            "confidence": 0.85
        }
    }
    
    for design, info in patterns.items():
        if re.search(info["pattern"], text, re.I):
            return design, info["confidence"]
    return "Not clearly specified", 0.0

def extract_sample_size(text):
    """Extract sample size with context"""
    patterns = [
        r"(?:sample size|n)\s*[=:]\s*(\d+(?:,\d+)?)",
        r"(\d+(?:,\d+)?)\s*(?:participants|patients|subjects|individuals)",
        r"total of\s+(\d+(?:,\d+)?)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1).replace(",", "")
    return None

def extract_statistical_tests(text):
    """Extract mentioned statistical tests"""
    test_patterns = {
        "t-test": r"t[\s-]test|student[\s-]t",
        "ANOVA": r"ANOVA|analysis of variance",
        "Chi-square": r"chi[\s-]square|χ2",
        "Mann-Whitney": r"Mann[\s-]Whitney",
        "Wilcoxon": r"Wilcoxon",
        "Kruskal-Wallis": r"Kruskal[\s-]Wallis",
        "Pearson correlation": r"Pearson[\s-]correlation",
        "Spearman correlation": r"Spearman[\s-]correlation",
        "Logistic regression": r"logistic regression",
        "Linear regression": r"linear regression",
        "Cox regression": r"Cox regression|proportional hazards",
        "Mixed models": r"mixed[\s-]effects|multilevel"
    }
    
    found_tests = []
    for test, pattern in test_patterns.items():
        if re.search(pattern, text, re.I):
            found_tests.append(test)
    
    return found_tests

def assess_methodological_quality(text):
    """Initial methodological quality assessment"""
    quality_indicators = {
        "Clear objectives": bool(re.search(r"(?:aim|objective|purpose|hypothesis)", text, re.I)),
        "Ethical approval": bool(re.search(r"(?:ethics|IRB|institutional review|approval|consent)", text, re.I)),
        "Sample justification": bool(re.search(r"(?:power calculation|sample size calculation|justification)", text, re.I)),
        "Statistical software": bool(re.search(r"(?:SPSS|R|Stata|SAS|Python|JMP|GraphPad)", text, re.I)),
        "Conflict of interest": bool(re.search(r"(?:conflict of interest|competing interests|disclosure)", text, re.I)),
        "Funding source": bool(re.search(r"(?:funding|grant|support|sponsor)", text, re.I))
    }
    
    quality_score = sum(quality_indicators.values()) / len(quality_indicators)
    return quality_indicators, quality_score

def show():
    init_session()

    st.markdown("## 📄 **Manuscript Preview & Comprehensive Editorial Assessment**")
    
    text = st.session_state.get("raw_text")
    
    if not text or not st.session_state.file_uploaded:
        st.error("❌ No manuscript loaded. Please upload a document first.")
        if st.button("← Return to Upload"):
            st.session_state.page = 1
            st.rerun()
        return
    
    # ----------------------------- #
    # COMPREHENSIVE ANALYSIS
    # ----------------------------- #
    design, design_confidence = detect_study_design(text)
    sample_size = extract_sample_size(text)
    statistical_tests = extract_statistical_tests(text)
    quality_indicators, quality_score = assess_methodological_quality(text)
    
    # Section detection
    sections = ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]
    detected_sections = [sec for sec in sections if re.search(rf"\b{sec}\b", text, re.I)]
    
    # Table/figure detection
    tables = len(re.findall(r"\btable\s+\d+", text, re.I))
    figures = len(re.findall(r"\bfigure\s+\d+", text, re.I))
    
    st.markdown("---")
    
    # ----------------------------- #
    # MAIN TABS
    # ----------------------------- #
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 **Study Characteristics**",
        "📑 **Structural Analysis**",
        "🎯 **Guideline Mapping**",
        "🧠 **Quality Snapshot**",
        "⚙️ **Review Configuration**"
    ])
    
    # TAB 1: Study Characteristics
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧬 Study Design")
            st.info(f"**{design}**")
            if design_confidence > 0:
                st.progress(design_confidence, text=f"Detection confidence: {design_confidence*100:.0f}%")
        
        with col2:
            st.markdown("### 📊 Sample")
            if sample_size:
                st.metric("Sample Size", f"n = {int(sample_size):,}")
            else:
                st.warning("Sample size not clearly reported")
        
        st.markdown("### 📈 Statistical Tests Detected")
        if statistical_tests:
            st.write(", ".join(statistical_tests))
        else:
            st.warning("No specific statistical tests mentioned")
        
        st.markdown("### 🔬 Key Variables")
        variables = re.findall(r"\b(?:age|gender|sex|BMI|blood pressure|temperature|score)\b", text, re.I)
        if variables:
            unique_vars = list(set(variables))[:5]
            st.write(", ".join(unique_vars))
    
    # TAB 2: Structural Analysis
    with tab2:
        st.markdown("### 📑 Section Breakdown")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tables Detected", tables)
            st.metric("Figures Detected", figures)
        with col2:
            st.metric("Total Sections", len(detected_sections))
            word_count = len(text.split())
            st.metric("Word Count", f"{word_count:,}")
        
        st.markdown("### ✅ Detected Sections")
        for section in sections:
            if section in detected_sections:
                st.success(f"✓ {section}")
            else:
                st.warning(f"✗ {section} (not clearly identified)")
        
        if "Methods" not in detected_sections:
            st.error("⚠️ **Critical:** Methods section not clearly identified - methodology review will be limited")
        if "Results" not in detected_sections:
            st.error("⚠️ **Critical:** Results section not clearly identified - results review will be limited")
    
    # TAB 3: Guideline Mapping
    with tab3:
        st.markdown("### 🎯 Recommended Reporting Guidelines")
        
        guideline_map = {
            "Randomized Controlled Trial": "CONSORT (Consolidated Standards of Reporting Trials)",
            "Cohort Study": "STROBE (Strengthening the Reporting of Observational Studies)",
            "Case-Control Study": "STROBE",
            "Cross-Sectional Study": "STROBE",
            "Systematic Review": "PRISMA (Preferred Reporting Items for Systematic Reviews)",
            "Qualitative Study": "COREQ (Consolidated Criteria for Reporting Qualitative Research)"
        }
        
        matched_guideline = None
        for study_type, guideline in guideline_map.items():
            if study_type in design:
                matched_guideline = guideline
                break
        
        if matched_guideline:
            st.success(f"**Recommended:** {matched_guideline}")
            st.info(f"This manuscript appears to follow a {design} design, which should adhere to {matched_guideline} guidelines.")
        else:
            st.info("General reporting guidelines: Consider EQUATOR Network resources")
        
        st.markdown("### 📋 Checklist Items to Verify")
        if "RCT" in design:
            st.write("- [ ] Randomization method and sequence generation")
            st.write("- [ ] Allocation concealment mechanism")
            st.write("- [ ] Blinding procedures (participants, personnel, outcome assessors)")
            st.write("- [ ] Intention-to-treat analysis")
            st.write("- [ ] Participant flow diagram")
        elif "Cohort" in design or "Case-Control" in design:
            st.write("- [ ] Participant selection criteria")
            st.write("- [ ] Confounding variable identification and control")
            st.write("- [ ] Follow-up duration and completeness")
            st.write("- [ ] Missing data handling")
        elif "Systematic" in design:
            st.write("- [ ] Comprehensive search strategy")
            st.write("- [ ] Study selection process (PRISMA flow)")
            st.write("- [ ] Risk of bias assessment")
            st.write("- [ ] Heterogeneity assessment")
    
    # TAB 4: Quality Snapshot
    with tab4:
        st.markdown("### 🧠 Preliminary Quality Indicators")
        
        col1, col2 = st.columns(2)
        
        with col1:
            for indicator, present in list(quality_indicators.items())[:3]:
                if present:
                    st.success(f"✓ {indicator}")
                else:
                    st.warning(f"✗ {indicator}")
        
        with col2:
            for indicator, present in list(quality_indicators.items())[3:]:
                if present:
                    st.success(f"✓ {indicator}")
                else:
                    st.warning(f"✗ {indicator}")
        
        st.markdown("### 📊 Initial Quality Score")
        st.progress(quality_score, text=f"Methodological completeness: {quality_score*100:.0f}%")
        
        if quality_score < 0.5:
            st.error("⚠️ **Low preliminary quality score** - Expect significant revision recommendations")
        elif quality_score < 0.7:
            st.warning("⚠️ **Moderate quality** - Several methodological improvements likely needed")
        else:
            st.success("✅ **Good preliminary quality** - Methodology appears reasonably complete")
    
    # TAB 5: Review Configuration
    with tab5:
        st.markdown("### ⚙️ Configure Deep Review Parameters")
        
        # Guideline selection
        guideline_options = ["CONSORT", "STROBE", "PRISMA", "COREQ", "General"]
        
        # Auto-select based on design
        auto_select = []
        if "RCT" in design:
            auto_select = ["CONSORT"]
        elif "Cohort" in design or "Case-Control" in design or "Cross-Sectional" in design:
            auto_select = ["STROBE"]
        elif "Systematic" in design:
            auto_select = ["PRISMA"]
        elif "Qualitative" in design:
            auto_select = ["COREQ"]
        
        selected = st.multiselect(
            "**Select review guidelines to apply**",
            guideline_options,
            default=auto_select if auto_select else ["General"],
            help="Selecting appropriate guidelines will enhance the specificity of the review"
        )
        
        st.session_state.selected_guidelines = selected
        
        st.markdown("### 🎯 Review Focus Areas")
        
        col1, col2 = st.columns(2)
        with col1:
            review_depth = st.select_slider(
                "**Review depth**",
                options=["Standard", "Detailed", "Comprehensive"],
                value="Detailed"
            )
        with col2:
            critical_focus = st.multiselect(
                "**Critical focus areas**",
                ["Bias assessment", "Sample size justification", "Statistical assumptions", 
                 "Missing data handling", "Multiple comparisons", "Effect sizes"],
                default=["Sample size justification"]
            )
        
        st.markdown("---")
        
        if st.button("🚀 **Begin Comprehensive Editorial Review**", type="primary", use_container_width=True):
            # Store review parameters
            st.session_state.review_depth = review_depth
            st.session_state.critical_focus = critical_focus
            st.session_state.page = 3
            st.rerun()
    
    st.markdown("---")
    st.caption("🔍 This preview provides an initial manuscript assessment to guide the detailed editorial review")