# page6_comprehensive_summary.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

def show():
    st.markdown("## 📊 **Comprehensive Editorial Summary & Decision Report**")
    
    # Check for required data
    if "raw_text" not in st.session_state:
        st.error("❌ No manuscript loaded. Please return to upload page.")
        if st.button("← Return to Upload"):
            st.session_state.page = 1
            st.rerun()
        return
    
    # Retrieve all analysis results
    methodology_results = st.session_state.get("methodology_results", {})
    statistics_results = st.session_state.get("statistics_results", {})
    results_reporting_results = st.session_state.get("results_reporting_results", {})
    
    # Check if analyses have been completed
    if not methodology_results or not statistics_results or not results_reporting_results:
        st.warning("⚠️ Not all reviews have been completed. Please complete all review sections first.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Go to Methodology Review", use_container_width=True):
                st.session_state.page = 3
                st.rerun()
        with col2:
            if st.button("Go to Statistics Review", use_container_width=True):
                st.session_state.page = 4
                st.rerun()
        with col3:
            if st.button("Go to Results Review", use_container_width=True):
                st.session_state.page = 5
                st.rerun()
        return
    
    # Calculate comprehensive scores
    methodology_score = methodology_results.get("overall_score", 0)
    statistics_score = statistics_results.get("overall_score", 0)
    results_score = results_reporting_results.get("overall_score", 0)
    
    # Weighted overall score (Methodology 40%, Statistics 35%, Results 25%)
    overall_score = (methodology_score * 0.4 + statistics_score * 0.35 + results_score * 0.25)
    
    # Determine editorial decision
    editorial_decision = determine_editorial_decision(overall_score, methodology_results, statistics_results, results_reporting_results)
    
    # Collect all issues
    all_critical_issues = []
    all_critical_issues.extend(methodology_results.get("critical_gaps", []))
    all_critical_issues.extend(statistics_results.get("critical_gaps", []))
    all_critical_issues.extend(results_reporting_results.get("critical_gaps", []))
    
    all_major_issues = []
    all_major_issues.extend([i for i in methodology_results.get("issues", []) if hasattr(i, 'severity') and i.severity == "major"])
    all_major_issues.extend([i for i in statistics_results.get("issues", []) if hasattr(i, 'severity') and i.severity == "major"])
    all_major_issues.extend([i for i in results_reporting_results.get("issues", []) if hasattr(i, 'severity') and i.severity == "major"])
    
    # Collect strengths
    all_strengths = []
    all_strengths.extend(methodology_results.get("strengths", [])[:3])
    all_strengths.extend(statistics_results.get("strengths", [])[:3])
    all_strengths.extend(results_reporting_results.get("strengths", [])[:3])
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 **Executive Dashboard**",
        "⚖️ **Editorial Decision**",
        "📋 **Comprehensive Report**",
        "📥 **Download Package**",
        "🔄 **Export & Submit**"
    ])
    
    # TAB 1: Executive Dashboard
    with tab1:
        st.markdown("### 🎯 Overall Quality Dashboard")
        
        # Create gauge chart for overall score
        col1, col2 = st.columns([1, 2])
        
        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=overall_score * 100,
                title={"text": "Overall Quality Score (%)"},
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": get_score_color(overall_score)},
                    "steps": [
                        {"range": [0, 50], "color": "#ff6b6b"},
                        {"range": [50, 70], "color": "#ffd93d"},
                        {"range": [70, 85], "color": "#6bcf7f"},
                        {"range": [85, 100], "color": "#2ecc71"}
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": overall_score * 100
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Section Scores")
            section_data = pd.DataFrame({
                "Section": ["Methodology", "Statistics", "Results Reporting"],
                "Score": [methodology_score * 100, statistics_score * 100, results_score * 100],
                "Color": [get_score_color(methodology_score), 
                         get_score_color(statistics_score), 
                         get_score_color(results_score)]
            })
            
            fig = px.bar(section_data, x="Section", y="Score", 
                        color="Score", color_continuous_scale="RdYlGn",
                        range_y=[0, 100],
                        title="Section-wise Performance")
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Critical Issues", len(all_critical_issues), delta="Must address" if all_critical_issues else "None", delta_color="inverse")
        with col2:
            st.metric("Major Issues", len(all_major_issues))
        with col3:
            st.metric("Strengths Identified", len(all_strengths))
        with col4:
            decision_emoji = "✅" if editorial_decision["decision"] == "Accept" else "⚠️" if editorial_decision["decision"] in ["Minor Revision", "Major Revision"] else "❌"
            st.metric("Editorial Decision", f"{decision_emoji} {editorial_decision['decision']}")
        
        # Radar chart for detailed comparison
        st.markdown("### 🎨 Detailed Component Analysis")
        
        components = {
            "Study Design": methodology_results.get("section_scores", {}).get("study_design", 0) * 100,
            "Participants": methodology_results.get("section_scores", {}).get("participants", 0) * 100,
            "Bias Control": methodology_results.get("section_scores", {}).get("bias_control", 0) * 100,
            "Descriptive Stats": statistics_results.get("section_scores", {}).get("descriptive_statistics", 0) * 100,
            "Inferential Stats": statistics_results.get("section_scores", {}).get("inferential_statistics", 0) * 100,
            "Effect Sizes": statistics_results.get("section_scores", {}).get("effect_sizes", 0) * 100,
            "Completeness": results_reporting_results.get("section_scores", {}).get("completeness", 0) * 100,
            "Transparency": results_reporting_results.get("section_scores", {}).get("transparency", 0) * 100
        }
        
        fig = go.Figure(data=go.Scatterpolar(
            r=list(components.values()),
            theta=list(components.keys()),
            fill='toself',
            marker=dict(color='#2ecc71', size=8),
            line=dict(color='#27ae60', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100]),
                angularaxis=dict(tickfont=dict(size=10))
            ),
            showlegend=False,
            height=450,
            title="Component Quality Heatmap"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Editorial Decision
    with tab2:
        st.markdown("### ⚖️ Final Editorial Decision")
        
        # Decision card
        decision_color = {
            "Accept": "#2ecc71",
            "Minor Revision": "#f39c12",
            "Major Revision": "#e67e22",
            "Reject": "#e74c3c"
        }.get(editorial_decision["decision"], "#95a5a6")
        
        st.markdown(f"""
        <div style="background-color: {decision_color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {decision_color};">
            <h3 style="color: {decision_color}; margin: 0;">Decision: {editorial_decision["decision"]}</h3>
            <p style="margin-top: 10px;"><strong>Confidence:</strong> {editorial_decision["confidence"]:.0%}</p>
            <p><strong>Justification:</strong> {editorial_decision["justification"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed decision factors
        st.markdown("### 📊 Decision Factors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Positive Factors")
            if all_strengths:
                for strength in all_strengths[:5]:
                    st.success(f"• {strength}")
            else:
                st.info("No major strengths identified")
        
        with col2:
            st.markdown("#### ⚠️ Risk Factors")
            if all_critical_issues:
                for issue in all_critical_issues[:5]:
                    if isinstance(issue, str):
                        st.error(f"• {issue}")
                    else:
                        st.error(f"• {issue.description if hasattr(issue, 'description') else str(issue)}")
            else:
                st.success("No critical risk factors identified")
        
        # Revision requirements
        if editorial_decision["decision"] in ["Minor Revision", "Major Revision"]:
            st.markdown("---")
            st.markdown("### 📝 Required Revisions")
            
            revision_items = []
            for issue in all_critical_issues[:3]:
                if isinstance(issue, str):
                    revision_items.append(f"- [ ] CRITICAL: {issue}")
                else:
                    revision_items.append(f"- [ ] CRITICAL: {issue.description if hasattr(issue, 'description') else str(issue)}")
            
            for issue in all_major_issues[:5]:
                if isinstance(issue, str):
                    revision_items.append(f"- [ ] MAJOR: {issue}")
                else:
                    revision_items.append(f"- [ ] MAJOR: {issue.description if hasattr(issue, 'description') else str(issue)}")
            
            st.markdown("\n".join(revision_items))
    
    # TAB 3: Comprehensive Report
    with tab3:
        st.markdown("### 📄 Complete Editorial Review Report")
        
        comprehensive_report = generate_comprehensive_report(
            filename=st.session_state.get("filename", "Unknown"),
            methodology_results=methodology_results,
            statistics_results=statistics_results,
            results_reporting_results=results_reporting_results,
            editorial_decision=editorial_decision,
            overall_score=overall_score
        )
        
        st.markdown(comprehensive_report)
        
        # Download button for comprehensive report
        st.download_button(
            label="📥 Download Comprehensive Report (Text)",
            data=comprehensive_report,
            file_name=f"MERIT_comprehensive_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # TAB 4: Download Package
    with tab4:
        st.markdown("### 📦 Complete Review Package")
        
        # Generate JSON summary
        json_summary = {
            "manuscript": {
                "filename": st.session_state.get("filename", "Unknown"),
                "review_date": datetime.now().isoformat(),
                "selected_guidelines": st.session_state.get("selected_guidelines", [])
            },
            "scores": {
                "methodology": methodology_score,
                "statistics": statistics_score,
                "results_reporting": results_score,
                "overall": overall_score
            },
            "editorial_decision": editorial_decision,
            "critical_issues_count": len(all_critical_issues),
            "major_issues_count": len(all_major_issues),
            "strengths_count": len(all_strengths)
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Download as JSON")
            st.download_button(
                label="📥 JSON Summary",
                data=json.dumps(json_summary, indent=2),
                file_name=f"review_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown("#### 📄 Download Individual Reports")
            if methodology_results.get("methodology_report"):
                st.download_button(
                    label="📋 Methodology Report",
                    data=methodology_results["methodology_report"],
                    file_name="methodology_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("#### 📊 Download as CSV")
            scores_df = pd.DataFrame([
                {"Section": "Methodology", "Score": methodology_score},
                {"Section": "Statistics", "Score": statistics_score},
                {"Section": "Results Reporting", "Score": results_score},
                {"Section": "Overall", "Score": overall_score}
            ])
            st.download_button(
                label="📥 Scores CSV",
                data=scores_df.to_csv(index=False),
                file_name="scores.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            if statistics_results.get("statistics_report"):
                st.download_button(
                    label="📋 Statistics Report",
                    data=statistics_results["statistics_report"],
                    file_name="statistics_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Create ZIP option (simulated - would need zipfile library)
        st.markdown("---")
        st.info("💡 **Tip:** All reports can be downloaded individually above. For a complete package, download each report separately.")
    
    # TAB 5: Export & Submit
    with tab5:
        st.markdown("### 📤 Export & Submission")
        
        st.markdown("#### 📧 Email Report")
        
        with st.form("email_form"):
            recipient_email = st.text_input("Recipient Email", placeholder="editor@journal.com")
            reviewer_notes = st.text_area("Reviewer Notes (Optional)", 
                                         placeholder="Add any additional comments for the editor...",
                                         height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                include_methodology = st.checkbox("Include Methodology Report", value=True)
            with col2:
                include_statistics = st.checkbox("Include Statistics Report", value=True)
            
            submitted = st.form_submit_button("📧 Generate Email Content", use_container_width=True)
            
            if submitted:
                email_content = generate_email_content(
                    recipient=recipient_email,
                    filename=st.session_state.get("filename", "Unknown"),
                    decision=editorial_decision["decision"],
                    justification=editorial_decision["justification"],
                    overall_score=overall_score,
                    critical_issues=len(all_critical_issues),
                    reviewer_notes=reviewer_notes
                )
                
                st.markdown("#### 📧 Email Preview")
                st.code(email_content, language="markdown")
                
                st.download_button(
                    label="📥 Download Email Content",
                    data=email_content,
                    file_name="editorial_email.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        # Start new review
        st.markdown("#### 🔄 Start New Review")
        
        if st.button("🔄 Begin New Manuscript Review", type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 1
            st.rerun()
    
    # Navigation footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Results Review", use_container_width=True):
            st.session_state.page = 5
            st.rerun()

# Helper functions
def get_score_color(score):
    """Return color based on score"""
    if score >= 0.85:
        return "#2ecc71"  # Green
    elif score >= 0.70:
        return "#6bcf7f"  # Light green
    elif score >= 0.60:
        return "#ffd93d"  # Yellow
    elif score >= 0.50:
        return "#f39c12"  # Orange
    else:
        return "#e74c3c"  # Red

def determine_editorial_decisoon(overall_score, methodology_results, statistics_results, results_reporting_results):
    """Determine editorial decision based on comprehensive analysis"""
    
    critical_issues_count = len(methodology_results.get("critical_gaps", [])) + \
                           len(statistics_results.get("critical_gaps", [])) + \
                           len(results_reporting_results.get("critical_gaps", []))
    
    spin_detected = results_reporting_results.get("spin_detected", False)
    common_errors = len(statistics_results.get("common_errors", []))
    
    if overall_score >= 0.80 and critical_issues_count == 0:
        decision = "Accept"
        confidence = 0.95
        justification = "Methodologically sound with complete and transparent reporting. No critical issues identified."
    elif overall_score >= 0.75 and critical_issues_count <= 1 and not spin_detected:
        decision = "Accept"
        confidence = 0.85
        justification = "High-quality manuscript with minor, addressable concerns."
    elif overall_score >= 0.65 and critical_issues_count <= 2:
        decision = "Minor Revision"
        confidence = 0.80
        justification = "Generally sound methodology with some reporting gaps that can be addressed with minor revisions."
    elif overall_score >= 0.50 and critical_issues_count <= 4:
        decision = "Major Revision"
        confidence = 0.75
        justification = "Significant methodological or reporting gaps requiring substantial revision before reconsideration."
    elif overall_score >= 0.40:
        decision = "Major Revision"
        confidence = 0.70
        justification = "Major deficiencies identified. Substantial revision required with potential need for additional analyses."
    else:
        decision = "Reject"
        confidence = 0.85
        justification = "Fundamental methodological flaws and/or critical reporting deficiencies that cannot be addressed through revision."
    
    # Adjust for specific issues
    if spin_detected and decision != "Reject":
        decision = "Major Revision"
        justification += " Additionally, results reporting shows evidence of spin/overinterpretation."
    
    if common_errors >= 3 and decision != "Reject":
        decision = "Major Revision"
        justification += " Multiple statistical errors identified requiring correction."
    
    return {
        "decision": decision,
        "justification": justification,
        "confidence": confidence
    }

def generate_comprehensive_report(filename, methodology_results, statistics_results, results_reporting_results, editorial_decision, overall_score):
    """Generate comprehensive editorial report"""
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("MERIT COMPREHENSIVE EDITORIAL REVIEW REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append(f"Manuscript: {filename}")
    report_lines.append(f"Review Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Executive summary
    report_lines.append("-" * 40)
    report_lines.append("EXECUTIVE SUMMARY")
    report_lines.append("-" * 40)
    report_lines.append(f"Overall Quality Score: {overall_score:.1%}")
    report_lines.append(f"Editorial Decision: {editorial_decision['decision']}")
    report_lines.append(f"Decision Confidence: {editorial_decision['confidence']:.0%}")
    report_lines.append("")
    report_lines.append(f"Justification: {editorial_decision['justification']}")
    report_lines.append("")
    
    # Section scores
    report_lines.append("-" * 40)
    report_lines.append("SECTION SCORES")
    report_lines.append("-" * 40)
    report_lines.append(f"Methodology Review: {methodology_results.get('overall_score', 0):.1%}")
    report_lines.append(f"Statistics Review: {statistics_results.get('overall_score', 0):.1%}")
    report_lines.append(f"Results Reporting Review: {results_reporting_results.get('overall_score', 0):.1%}")
    report_lines.append("")
    
    # Critical issues
    all_critical = []
    all_critical.extend(methodology_results.get("critical_gaps", []))
    all_critical.extend(statistics_results.get("critical_gaps", []))
    all_critical.extend(results_reporting_results.get("critical_gaps", []))
    
    if all_critical:
        report_lines.append("-" * 40)
        report_lines.append("CRITICAL ISSUES (Must Address)")
        report_lines.append("-" * 40)
        for i, issue in enumerate(all_critical, 1):
            if isinstance(issue, str):
                report_lines.append(f"{i}. {issue}")
            else:
                report_lines.append(f"{i}. {issue.description if hasattr(issue, 'description') else str(issue)}")
        report_lines.append("")
    
    # Strengths
    all_strengths = []
    all_strengths.extend(methodology_results.get("strengths", [])[:3])
    all_strengths.extend(statistics_results.get("strengths", [])[:3])
    all_strengths.extend(results_reporting_results.get("strengths", [])[:3])
    
    if all_strengths:
        report_lines.append("-" * 40)
        report_lines.append("KEY STRENGTHS")
        report_lines.append("-" * 40)
        for strength in all_strengths:
            report_lines.append(f"✓ {strength}")
        report_lines.append("")
    
    # Statistical errors
    common_errors = statistics_results.get("common_errors", [])
    if common_errors:
        report_lines.append("-" * 40)
        report_lines.append("IDENTIFIED STATISTICAL ERRORS")
        report_lines.append("-" * 40)
        for error in common_errors:
            report_lines.append(f"⚠️ {error}")
        report_lines.append("")
    
    # Final recommendations
    report_lines.append("-" * 40)
    report_lines.append("FINAL RECOMMENDATIONS")
    report_lines.append("-" * 40)
    
    if editorial_decision["decision"] == "Accept":
        report_lines.append("The manuscript is recommended for acceptance in its current form.")
        report_lines.append("Minor copyediting may still be required before publication.")
    elif editorial_decision["decision"] == "Minor Revision":
        report_lines.append("The manuscript requires minor revisions before acceptance.")
        report_lines.append("Please address the identified issues and provide a point-by-point response.")
    elif editorial_decision["decision"] == "Major Revision":
        report_lines.append("The manuscript requires major revisions before reconsideration.")
        report_lines.append("Please address all critical and major issues identified in this report.")
        report_lines.append("A revised manuscript with tracked changes is required for resubmission.")
    else:  # Reject
        report_lines.append("The manuscript is not recommended for publication in its current form.")
        report_lines.append("The identified issues are too substantial to address through revision.")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("End of Report")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)

def generate_email_content(recipient, filename, decision, justification, overall_score, critical_issues, reviewer_notes):
    """Generate email content for editor"""
    
    email = f"""To: {recipient if recipient else '[Editor Email]'}
Subject: MERIT Editorial Review: {filename}

Dear Editor,

Please find below the automated editorial review summary for the manuscript "{filename}".

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REVIEW SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Quality Score: {overall_score:.1%}
Editorial Decision: {decision}

Justification:
{justification}

Critical Issues Identified: {critical_issues}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This automated review assessed three key domains:
• Methodology integrity and completeness
• Statistical analysis appropriateness and reporting
• Results presentation and transparency

Please refer to the attached detailed reports for comprehensive findings.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REVIEWER NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{reviewer_notes if reviewer_notes else 'No additional notes provided.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This review was generated using MERIT (Manuscript Editorial Review & Intelligence Tool).
Please use this report as a guide for your editorial decision-making process.

Attachments: Comprehensive Review Report, Methodology Report, Statistics Report, Results Report

Best regards,
MERIT Editorial System
"""
    return email

# Fix function name typo
def determine_editorial_decision(overall_score, methodology_results, statistics_results, results_reporting_results):
    """Determine editorial decision based on comprehensive analysis"""
    return determine_editorial_decisoon(overall_score, methodology_results, statistics_results, results_reporting_results)