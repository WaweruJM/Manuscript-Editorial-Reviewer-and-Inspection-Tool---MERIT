# page3_methodology_review.py
import streamlit as st
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class MethodologyIssue:
    category: str
    severity: str  # critical, major, minor, suggestion
    description: str
    location: str
    recommendation: str
    guideline_reference: str

class DeepMethodologyAnalyzer:
    """Advanced methodology analyzer with comprehensive assessment"""
    
    def __init__(self):
        self.methodology_components = {
            "study_design": {
                "weight": 0.25,
                "elements": [
                    "design_specification", "study_setting", "study_duration", 
                    "design_justification", "comparison_groups"
                ]
            },
            "participants": {
                "weight": 0.25,
                "elements": [
                    "inclusion_criteria", "exclusion_criteria", "recruitment_method",
                    "sampling_strategy", "sample_size_calculation", "power_analysis"
                ]
            },
            "intervention_exposure": {
                "weight": 0.15,
                "elements": [
                    "intervention_description", "dosing_regimen", "administration_method",
                    "adherence_assessment", "concomitant_treatments"
                ]
            },
            "outcome_measures": {
                "weight": 0.15,
                "elements": [
                    "primary_outcome", "secondary_outcomes", "measurement_method",
                    "validity_evidence", "reliability_evidence", "assessment_timing"
                ]
            },
            "bias_control": {
                "weight": 0.20,
                "elements": [
                    "randomization_method", "allocation_concealment", "blinding_procedures",
                    "confounding_handling", "attrition_handling", "contamination_prevention"
                ]
            }
        }
        
        self.severity_weights = {"critical": 0, "major": 0.5, "minor": 0.75, "suggestion": 0.9}
    
    def analyze(self, text: str) -> Dict:
        """Perform comprehensive methodology analysis"""
        
        results = {
            "section_scores": {},
            "overall_score": 0.0,
            "issues": [],
            "strengths": [],
            "critical_gaps": [],
            "detailed_feedback": "",
            "methodology_report": ""
        }
        
        # Analyze each component
        for component, config in self.methodology_components.items():
            component_score, component_issues, component_strengths = self._analyze_component(
                text, component, config
            )
            results["section_scores"][component] = component_score
            results["issues"].extend(component_issues)
            results["strengths"].extend(component_strengths)
            results["overall_score"] += component_score * config["weight"]
        
        # Classify critical issues
        results["critical_gaps"] = [i for i in results["issues"] if i.severity == "critical"]
        
        # Generate detailed narrative report
        results["methodology_report"] = self._generate_narrative_report(results)
        
        return results
    
    def _analyze_component(self, text: str, component: str, config: Dict) -> Tuple[float, List, List]:
        """Analyze a specific methodology component"""
        
        element_scores = []
        issues = []
        strengths = []
        
        for element in config["elements"]:
            found, evidence, quality_score = self._check_element(text, element, component)
            
            if found:
                element_scores.append(quality_score)
                if quality_score > 0.8:
                    strengths.append(f"✓ **{self._format_element_name(element)}**: {evidence[:150]}")
            else:
                severity = "critical" if element in ["study_design", "sample_size_calculation", "inclusion_criteria"] else "major"
                issues.append(MethodologyIssue(
                    category=component,
                    severity=severity,
                    description=f"Missing or incomplete: {self._format_element_name(element)}",
                    location=f"{component.capitalize()} section",
                    recommendation=self._get_recommendation(element, component),
                    guideline_reference=self._get_guideline_reference(element)
                ))
        
        component_score = sum(element_scores) / len(config["elements"]) if element_scores else 0
        return component_score, issues, strengths
    
    def _check_element(self, text: str, element: str, component: str) -> Tuple[bool, str, float]:
        """Check for element presence and assess quality"""
        
        patterns = {
            "design_specification": r"(randomized|cohort|case-control|cross-sectional|qualitative|mixed[\s-]methods|quasi-experimental)",
            "study_setting": r"(hospital|clinic|university|community|primary care|tertiary care|academic medical center)",
            "inclusion_criteria": r"(inclusion criteria|eligible participants|enrolled if|included if)",
            "exclusion_criteria": r"(exclusion criteria|excluded if|not eligible)",
            "sample_size_calculation": r"(sample size calculation|power calculation|required sample size|powered to detect)",
            "power_analysis": r"(power|β|beta|type ii error)",
            "randomization_method": r"(randomiz(?:ed|ation)|random assignment|random number|computer-generated)",
            "allocation_concealment": r"(allocation concealment|sealed envelope|central randomization)",
            "blinding_procedures": r"(blind|masked|double-blind|single-blind|outcome assessor blind)",
            "primary_outcome": r"(primary outcome|primary endpoint|main outcome measure)",
            "validity_evidence": r"(validated|validity|previously validated|standardized)"
        }
        
        if element in patterns:
            match = re.search(patterns[element], text, re.I)
            if match:
                # Extract context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Assess quality
                quality_score = self._assess_quality(context)
                return True, context, quality_score
        
        return False, "", 0.0
    
    def _assess_quality(self, context: str) -> float:
        """Assess quality of description"""
        score = 0.7  # Base score for presence
        
        # Quality indicators
        if re.search(r"\d+", context):  # Contains numbers
            score += 0.1
        if re.search(r"(?:e\.g\.|i\.e\.|for example|specifically)", context, re.I):
            score += 0.05
        if re.search(r"\([^)]+\)", context):  # Parenthetical details
            score += 0.05
        if len(context.split()) > 20:  # Sufficient detail
            score += 0.1
        
        return min(1.0, score)
    
    def _format_element_name(self, element: str) -> str:
        """Format element name for display"""
        return element.replace("_", " ").title()
    
    def _get_recommendation(self, element: str, component: str) -> str:
        """Generate specific recommendation"""
        recommendations = {
            "design_specification": "Clearly state the study design and provide justification for its selection",
            "sample_size_calculation": "Provide detailed sample size calculation including expected effect size, power (typically 80%), and alpha level (typically 0.05)",
            "inclusion_criteria": "Specify all inclusion criteria including demographic, clinical, and temporal parameters",
            "randomization_method": "Describe the randomization sequence generation method (e.g., computer-generated random numbers) and who generated it",
            "allocation_concealment": "Explain how allocation was concealed until assignment (e.g., sequentially numbered opaque sealed envelopes)",
            "blinding_procedures": "Specify who was blinded (participants, care providers, outcome assessors, analysts) and how blinding was maintained",
            "primary_outcome": "Clearly define the primary outcome measure, including measurement method, timing, and unit of analysis"
        }
        return recommendations.get(element, f"Provide comprehensive description of {self._format_element_name(element)}")
    
    def _get_guideline_reference(self, element: str) -> str:
        """Get relevant guideline reference"""
        references = {
            "randomization_method": "CONSORT Item 8a",
            "allocation_concealment": "CONSORT Item 9",
            "blinding_procedures": "CONSORT Item 11a",
            "sample_size_calculation": "CONSORT Item 7a",
            "primary_outcome": "CONSORT Item 6a"
        }
        return references.get(element, "EQUATOR Network guidelines")
    
    def _generate_narrative_report(self, results: Dict) -> str:
        """Generate comprehensive narrative methodology report"""
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("METHODOLOGY REVIEW REPORT")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        # Overall assessment
        overall_score = results["overall_score"]
        if overall_score >= 0.8:
            grade = "EXCELLENT"
            assessment = "The methodology is thoroughly described and follows best practices."
        elif overall_score >= 0.7:
            grade = "GOOD"
            assessment = "The methodology is largely complete with minor gaps that can be addressed."
        elif overall_score >= 0.6:
            grade = "FAIR"
            assessment = "The methodology has notable gaps requiring moderate revision."
        elif overall_score >= 0.5:
            grade = "POOR"
            assessment = "The methodology has major deficiencies requiring substantial revision."
        else:
            grade = "VERY POOR"
            assessment = "The methodology is critically deficient and may require major restructuring or rejection."
        
        report_lines.append(f"OVERALL GRADE: {grade}")
        report_lines.append(f"SCORE: {overall_score:.1%}")
        report_lines.append("")
        report_lines.append(f"ASSESSMENT: {assessment}")
        report_lines.append("")
        
        # Section scores
        report_lines.append("-" * 50)
        report_lines.append("COMPONENT SCORES")
        report_lines.append("-" * 50)
        for component, score in results["section_scores"].items():
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            report_lines.append(f"{component.replace('_', ' ').title():20} {bar} {score:.1%}")
        report_lines.append("")
        
        # Strengths
        if results["strengths"]:
            report_lines.append("-" * 50)
            report_lines.append("METHODOLOGICAL STRENGTHS")
            report_lines.append("-" * 50)
            for strength in results["strengths"][:5]:
                report_lines.append(strength)
            report_lines.append("")
        
        # Critical Issues
        critical_issues = [i for i in results["issues"] if i.severity == "critical"]
        if critical_issues:
            report_lines.append("-" * 50)
            report_lines.append("CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION")
            report_lines.append("-" * 50)
            for issue in critical_issues:
                report_lines.append(f"🔴 {issue.description}")
                report_lines.append(f"   → Recommendation: {issue.recommendation}")
                report_lines.append(f"   → Reference: {issue.guideline_reference}")
                report_lines.append("")
        
        # Major Issues
        major_issues = [i for i in results["issues"] if i.severity == "major"]
        if major_issues:
            report_lines.append("-" * 50)
            report_lines.append("MAJOR ISSUES")
            report_lines.append("-" * 50)
            for issue in major_issues[:5]:
                report_lines.append(f"🟠 {issue.description}")
                report_lines.append(f"   → {issue.recommendation}")
                report_lines.append("")
        
        # Summary recommendations
        report_lines.append("-" * 50)
        report_lines.append("SUMMARY RECOMMENDATIONS")
        report_lines.append("-" * 50)
        
        if critical_issues:
            report_lines.append(f"1. Address {len(critical_issues)} critical methodological gaps before proceeding")
        if major_issues:
            report_lines.append(f"2. Revise {len(major_issues)} major methodological descriptions")
        
        report_lines.append("3. Consider following relevant reporting guidelines (CONSORT/STROBE/PRISMA)")
        report_lines.append("4. Ensure all methodology elements are sufficiently detailed for replication")
        report_lines.append("")
        
        report_lines.append("=" * 70)
        report_lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)

def show():
    st.markdown("## 🧪 **Comprehensive Methodology Review**")
    
    if "raw_text" not in st.session_state:
        st.error("❌ No manuscript loaded. Please return to upload page.")
        if st.button("← Return to Upload"):
            st.session_state.page = 1
            st.rerun()
        return
    
    text = st.session_state.raw_text
    
    # Initialize and run analyzer
    analyzer = DeepMethodologyAnalyzer()
    
    with st.spinner("🔍 Performing deep methodology analysis... This may take a moment"):
        results = analyzer.analyze(text)
        st.session_state.methodology_results = results
    
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 **Executive Summary**",
        "📋 **Detailed Findings**",
        "📄 **Editorial Report**"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Overall Score")
            score = results["overall_score"]
            st.progress(score, text=f"{score:.1%}")
            
            if score >= 0.8:
                st.success("✅ **Grade: Excellent**")
            elif score >= 0.7:
                st.success("✅ **Grade: Good**")
            elif score >= 0.6:
                st.warning("⚠️ **Grade: Fair**")
            else:
                st.error("❌ **Grade: Needs Major Revision**")
        
        with col2:
            st.markdown("### Critical Issues")
            critical_count = len(results["critical_gaps"])
            if critical_count == 0:
                st.success(f"🎉 No critical issues found")
            else:
                st.error(f"🔴 {critical_count} critical issue(s) requiring attention")
        
        st.markdown("### Component Scores")
        for component, comp_score in results["section_scores"].items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(component.replace("_", " ").title())
            with col2:
                st.progress(comp_score, text=f"{comp_score:.1%}")
    
    with tab2:
        st.markdown("### ✅ Methodological Strengths")
        if results["strengths"]:
            for strength in results["strengths"][:8]:
                st.success(strength)
        else:
            st.info("No specific strengths identified")
        
        st.markdown("### ⚠️ Issues Requiring Attention")
        
        # Group by severity
        critical = [i for i in results["issues"] if i.severity == "critical"]
        major = [i for i in results["issues"] if i.severity == "major"]
        minor = [i for i in results["issues"] if i.severity == "minor"]
        
        if critical:
            st.markdown("#### 🔴 Critical Issues (Must Address)")
            for issue in critical:
                with st.expander(f"❌ {issue.description}"):
                    st.write(f"**Location:** {issue.location}")
                    st.write(f"**Recommendation:** {issue.recommendation}")
                    st.write(f"**Guideline:** {issue.guideline_reference}")
        
        if major:
            st.markdown("#### 🟠 Major Issues")
            for issue in major:
                with st.expander(f"⚠️ {issue.description}"):
                    st.write(f"**Recommendation:** {issue.recommendation}")
        
        if minor:
            st.markdown("#### 🟡 Minor Issues & Suggestions")
            for issue in minor[:5]:
                st.write(f"• {issue.description} → {issue.recommendation}")
    
    with tab3:
        st.markdown("### 📄 Complete Methodology Editorial Report")
        st.markdown("---")
        st.markdown(results["methodology_report"])
        
        # Download button for report
        st.download_button(
            label="📥 Download Methodology Report",
            data=results["methodology_report"],
            file_name=f"methodology_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Preview", use_container_width=True):
            st.session_state.page = 2
            st.rerun()
    with col2:
        if st.button("Proceed to Statistical Analysis →", type="primary", use_container_width=True):
            st.session_state.page = 4
            st.rerun()