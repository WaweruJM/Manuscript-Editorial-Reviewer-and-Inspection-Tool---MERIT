# PAGE5_Reporting_of_Results_Review.py
import streamlit as st
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from collections import Counter

@dataclass
class ReportingIssue:
    category: str
    severity: str  # critical, major, minor, suggestion
    description: str
    location: str
    recommendation: str
    best_practice: str

class DeepResultsAnalyzer:
    """Advanced results reporting analyzer with comprehensive assessment"""
    
    def __init__(self):
        self.reporting_components = {
            "completeness": {
                "weight": 0.30,
                "elements": [
                    "primary_outcomes_reported", "secondary_outcomes_reported", 
                    "adverse_events", "missing_data_accounted", "attrition_reported"
                ]
            },
            "transparency": {
                "weight": 0.25,
                "elements": [
                    "negative_results_reported", "exact_numbers_provided",
                    "confidence_intervals_included", "effect_sizes_reported"
                ]
            },
            "data_presentation": {
                "weight": 0.20,
                "elements": [
                    "tables_referenced", "figures_referenced", "appropriate_summaries",
                    "units_of_measurement", "denominators_clear"
                ]
            },
            "interpretation": {
                "weight": 0.15,
                "elements": [
                    "clinical_significance", "comparison_to_literature",
                    "limitations_acknowledged", "generalizability_discussed"
                ]
            },
            "selective_reporting": {
                "weight": 0.10,
                "elements": [
                    "all_outcomes_reported", "no_post_hoc_overinterpretation",
                    "subgroup_transparency", "sensitivity_analyses"
                ]
            }
        }
        
    def analyze(self, text: str) -> Dict:
        """Perform comprehensive results reporting analysis"""
        
        results = {
            "section_scores": {},
            "overall_score": 0.0,
            "issues": [],
            "strengths": [],
            "critical_gaps": [],
            "inconsistencies": [],
            "selective_reporting_indicators": [],
            "spin_detected": False,
            "results_report": ""
        }
        
        # Analyze each component
        for component, config in self.reporting_components.items():
            component_score, component_issues, component_strengths = self._analyze_component(
                text, component, config
            )
            results["section_scores"][component] = component_score
            results["issues"].extend(component_issues)
            results["strengths"].extend(component_strengths)
            results["overall_score"] += component_score * config["weight"]
        
        # Detect inconsistencies
        results["inconsistencies"] = self._detect_inconsistencies(text)
        
        # Detect selective reporting
        results["selective_reporting_indicators"] = self._detect_selective_reporting(text)
        
        # Detect spin
        results["spin_detected"] = self._detect_spin(text)
        
        # Classify critical issues
        results["critical_gaps"] = [i for i in results["issues"] if i.severity == "critical"]
        
        # Generate narrative report
        results["results_report"] = self._generate_narrative_report(results)
        
        return results
    
    def _analyze_component(self, text: str, component: str, config: Dict) -> Tuple[float, List, List]:
        """Analyze a specific reporting component"""
        
        element_scores = []
        issues = []
        strengths = []
        
        for element in config["elements"]:
            found, evidence, quality_score = self._check_element(text, element, component)
            
            if found:
                element_scores.append(quality_score)
                if quality_score > 0.7:
                    strengths.append(f"✓ **{self._format_element_name(element)}**: {evidence[:100]}...")
            else:
                severity = "critical" if element in ["primary_outcomes_reported", "negative_results_reported"] else "major"
                issues.append(ReportingIssue(
                    category=component,
                    severity=severity,
                    description=f"Missing or inadequate: {self._format_element_name(element)}",
                    location="Results section",
                    recommendation=self._get_recommendation(element),
                    best_practice=self._get_best_practice(element)
                ))
        
        component_score = sum(element_scores) / len(config["elements"]) if element_scores else 0
        return component_score, issues, strengths
    
    def _check_element(self, text: str, element: str, component: str) -> Tuple[bool, str, float]:
        """Check for reporting element presence and quality"""
        
        patterns = {
            "primary_outcomes_reported": r"(?:primary outcome|primary endpoint|main outcome)[\s\S]{0,100}(?:was|were|showed|demonstrated)",
            "secondary_outcomes_reported": r"(?:secondary outcome|secondary endpoint|exploratory outcome)",
            "adverse_events": r"(?:adverse event|side effect|safety|tolerability|serious adverse)",
            "missing_data_accounted": r"(?:missing data|loss to follow-up|attrition|dropout|withdrew)",
            "negative_results_reported": r"(?:no significant|non-significant|not significant|null finding|no association)",
            "exact_numbers_provided": r"\d+(?:\.\d+)?\s*\([\d\.,\s-]+\)|n\s*=\s*\d+",
            "confidence_intervals_included": r"(?:CI|confidence interval)\s*[=:]\s*\[?\d+\.?\d*\s*[,–-]\s*\d+\.?\d*\]?",
            "effect_sizes_reported": r"(?:effect size|cohen|hedges|eta|odds ratio|risk ratio|hazard ratio)",
            "tables_referenced": r"(?:Table|Tab\.)\s+\d+",
            "figures_referenced": r"(?:Figure|Fig\.)\s+\d+",
            "clinical_significance": r"(?:clinical significance|clinical importance|meaningful|practical significance)"
        }
        
        if element in patterns:
            match = re.search(patterns[element], text, re.I)
            if match:
                start = max(0, match.start() - 60)
                end = min(len(text), match.end() + 60)
                context = text[start:end].strip()
                quality_score = self._assess_quality(context, element)
                return True, context, quality_score
        
        return False, "", 0.0
    
    def _assess_quality(self, context: str, element: str) -> float:
        """Assess quality of results reporting"""
        score = 0.7
        
        if element == "confidence_intervals_included":
            if re.search(r"\d+\.?\d*\s*\([\d\.\s,-]+\)", context):
                score += 0.2
        elif element == "exact_numbers_provided":
            if re.search(r"\d+\.\d+", context):  # Decimal precision
                score += 0.1
            if re.search(r"\(n\s*=\s*\d+\)", context):
                score += 0.1
        
        if len(context.split()) > 25:
            score += 0.05
        
        return min(1.0, score)
    
    def _detect_inconsistencies(self, text: str) -> List[str]:
        """Detect internal inconsistencies in results reporting"""
        inconsistencies = []
        
        # Check for contradictory statements about significance
        significant_statements = re.findall(r"(?:significant|non-significant|p\s*[<>=]\s*0\.0[0-9]{1,2})", text, re.I)
        if len(significant_statements) > 10:
            # Look for contradictions within close proximity
            contradictions = re.findall(r"(?:significant[\s\S]{0,100}non-significant|non-significant[\s\S]{0,100}significant)", text, re.I)
            if contradictions:
                inconsistencies.append("Potential contradictory significance statements within close proximity")
        
        # Check for numbers that don't add up
        percentages = re.findall(r'(\d+(?:\.\d+)?)%', text)
        if len(percentages) > 3:
            # Simple check for percentages > 100
            invalid_percentages = [p for p in percentages if float(p) > 100]
            if invalid_percentages:
                inconsistencies.append(f"Invalid percentages detected (>100%): {', '.join(invalid_percentages[:3])}")
        
        # Check for table/figure references without actual tables
        table_refs = len(re.findall(r"Table\s+\d+", text, re.I))
        figure_refs = len(re.findall(r"Figure\s+\d+", text, re.I))
        
        if table_refs > 0 and table_refs < 3:
            inconsistencies.append(f"Only {table_refs} table reference(s) detected - ensure all tables are properly referenced")
        
        return inconsistencies
    
    def _detect_selective_reporting(self, text: str) -> List[str]:
        """Detect potential selective outcome reporting"""
        indicators = []
        
        # Check for 'data not shown'
        if re.search(r"data not shown|results not presented|not shown", text, re.I):
            indicators.append("'Data not shown' indicates potential selective reporting of favorable results")
        
        # Check for unexpected post-hoc analyses presented as confirmatory
        if re.search(r"post[\s-]hoc[\s\S]{0,100}(?:significant|found|observed)", text, re.I):
            indicators.append("Post-hoc analyses should be clearly labeled as exploratory, not confirmatory")
        
        # Check for missing expected outcomes
        methods_outcomes = re.findall(r"(?:we assessed|measured|recorded|collected)[\s\S]{0,100}([^.]{20,100}?)\.", text)
        results_outcomes = re.findall(r"(?:results?|findings?|analysis)[\s\S]{0,100}([^.]{20,100}?)\.", text)
        
        # Simple check: if methods mention outcomes but results don't reference them
        if len(methods_outcomes) > len(results_outcomes) + 2:
            indicators.append("Potential discrepancy between outcomes mentioned in methods and results sections")
        
        return indicators
    
    def _detect_spin(self, text: str) -> bool:
        """Detect spin or overinterpretation of results"""
        spin_patterns = [
            (r"trend[\s\S]{0,50}(?:towards?|to)", "Using 'trend' for non-significant results"),
            (r"borderline[\s\S]{0,50}significant", "Describing near-significant p-values as 'borderline significant'"),
            (r"close[\s\S]{0,50}to[\s\S]{0,50}significant", "Overinterpreting p-values close to significance"),
            (r"numerically[\s\S]{0,50}(?:higher|lower|greater)", "Emphasizing numerical differences without statistical support"),
            (r"failed[\s]?to[\s]?reach[\s\S]{0,50}significance", "Overemphasis on non-significant results"),
            (r"approached[\s\S]{0,50}significance", "Misleading description of non-significant results")
        ]
        
        for pattern, description in spin_patterns:
            if re.search(pattern, text, re.I):
                return True
        return False
    
    def _format_element_name(self, element: str) -> str:
        """Format element name for display"""
        return element.replace("_", " ").title()
    
    def _get_recommendation(self, element: str) -> str:
        """Generate specific recommendation"""
        recommendations = {
            "primary_outcomes_reported": "Clearly report results for all primary outcomes with appropriate statistical measures",
            "negative_results_reported": "Report negative/null results transparently - they are as important as positive findings",
            "confidence_intervals_included": "Include 95% confidence intervals for all effect estimates",
            "effect_sizes_reported": "Report effect sizes with interpretation (small/medium/large) for all primary comparisons",
            "missing_data_accounted": "Clearly account for missing data including numbers and handling methods",
            "clinical_significance": "Discuss clinical/practical significance alongside statistical significance"
        }
        return recommendations.get(element, f"Ensure {self._format_element_name(element)} is adequately reported")
    
    def _get_best_practice(self, element: str) -> str:
        """Get best practice guideline"""
        practices = {
            "confidence_intervals_included": "Best practice: Report 95% CIs for all primary effect estimates",
            "effect_sizes_reported": "Best practice: Report standardized effect sizes (Cohen's d, η², etc.)",
            "negative_results_reported": "Best practice: Report all outcomes regardless of statistical significance"
        }
        return practices.get(element, "Follow EQUATOR network reporting guidelines")
    
    def _generate_narrative_report(self, results: Dict) -> str:
        """Generate comprehensive results reporting report"""
        
        report_lines = []
        report_lines.append("=" * 75)
        report_lines.append("RESULTS REPORTING REVIEW REPORT")
        report_lines.append("=" * 75)
        report_lines.append("")
        
        # Overall assessment
        overall_score = results["overall_score"]
        if overall_score >= 0.8:
            grade = "EXCELLENT"
            assessment = "Results are reported completely, transparently, and without spin."
        elif overall_score >= 0.7:
            grade = "GOOD"
            assessment = "Results reporting is largely complete with minor gaps."
        elif overall_score >= 0.6:
            grade = "FAIR"
            assessment = "Results reporting has notable gaps requiring revision."
        elif overall_score >= 0.5:
            grade = "POOR"
            assessment = "Results reporting has major deficiencies."
        else:
            grade = "VERY POOR"
            assessment = "Results reporting is critically deficient."
        
        report_lines.append(f"OVERALL REPORTING GRADE: {grade}")
        report_lines.append(f"QUALITY SCORE: {overall_score:.1%}")
        report_lines.append("")
        report_lines.append(f"ASSESSMENT: {assessment}")
        report_lines.append("")
        
        # Component scores
        report_lines.append("-" * 50)
        report_lines.append("REPORTING COMPONENT SCORES")
        report_lines.append("-" * 50)
        for component, score in results["section_scores"].items():
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            component_name = component.replace("_", " ").title()
            report_lines.append(f"{component_name:25} {bar} {score:.1%}")
        report_lines.append("")
        
        # Spin detection
        if results["spin_detected"]:
            report_lines.append("-" * 50)
            report_lines.append("⚠️ SPIN DETECTED")
            report_lines.append("-" * 50)
            report_lines.append("The results section contains language that may overinterpret findings.")
            report_lines.append("Avoid describing non-significant results as 'trends' or 'borderline significant'.")
            report_lines.append("")
        
        # Selective reporting indicators
        if results["selective_reporting_indicators"]:
            report_lines.append("-" * 50)
            report_lines.append("SELECTIVE REPORTING INDICATORS")
            report_lines.append("-" * 50)
            for indicator in results["selective_reporting_indicators"]:
                report_lines.append(f"⚠️ {indicator}")
            report_lines.append("")
        
        # Inconsistencies
        if results["inconsistencies"]:
            report_lines.append("-" * 50)
            report_lines.append("INCONSISTENCIES DETECTED")
            report_lines.append("-" * 50)
            for inconsistency in results["inconsistencies"]:
                report_lines.append(f"⚠️ {inconsistency}")
            report_lines.append("")
        
        # Strengths
        if results["strengths"]:
            report_lines.append("-" * 50)
            report_lines.append("REPORTING STRENGTHS")
            report_lines.append("-" * 50)
            for strength in results["strengths"][:5]:
                report_lines.append(strength)
            report_lines.append("")
        
        # Critical issues
        critical_issues = [i for i in results["issues"] if i.severity == "critical"]
        if critical_issues:
            report_lines.append("-" * 50)
            report_lines.append("CRITICAL REPORTING ISSUES")
            report_lines.append("-" * 50)
            for issue in critical_issues:
                report_lines.append(f"🔴 {issue.description}")
                report_lines.append(f"   → Recommendation: {issue.recommendation}")
                report_lines.append(f"   → Best practice: {issue.best_practice}")
                report_lines.append("")
        
        # Major issues
        major_issues = [i for i in results["issues"] if i.severity == "major"]
        if major_issues:
            report_lines.append("-" * 50)
            report_lines.append("MAJOR REPORTING ISSUES")
            report_lines.append("-" * 50)
            for issue in major_issues[:5]:
                report_lines.append(f"🟠 {issue.description}")
                report_lines.append(f"   → {issue.recommendation}")
                report_lines.append("")
        
        # Summary recommendations
        report_lines.append("-" * 50)
        report_lines.append("SUMMARY RECOMMENDATIONS")
        report_lines.append("-" * 50)
        
        if results["spin_detected"]:
            report_lines.append("1. Revise spin language - present results objectively without overinterpretation")
        if results["selective_reporting_indicators"]:
            report_lines.append("2. Address selective reporting concerns - report all outcomes transparently")
        if not any("effect_sizes" in str(s) for s in results["strengths"]):
            report_lines.append("3. Include effect sizes with confidence intervals for all primary outcomes")
        if not any("negative_results" in str(s) for s in results["strengths"]):
            report_lines.append("4. Report negative/null results explicitly and transparently")
        
        report_lines.append("5. Ensure results align with pre-specified outcomes from methods section")
        report_lines.append("")
        
        report_lines.append("=" * 75)
        report_lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 75)
        
        return "\n".join(report_lines)


def show():
    st.markdown("## 📊 **Comprehensive Results Reporting Review**")
    
    if "raw_text" not in st.session_state:
        st.error("❌ No manuscript loaded. Please return to upload page.")
        if st.button("← Return to Upload"):
            st.session_state.page = 1
            st.rerun()
        return
    
    text = st.session_state.raw_text
    
    # Initialize and run analyzer
    analyzer = DeepResultsAnalyzer()
    
    with st.spinner("🔍 Analyzing results reporting quality... This may take a moment"):
        results = analyzer.analyze(text)
        st.session_state.results_reporting_results = results
    
    # Display results in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 **Executive Summary**",
        "🔍 **Detailed Findings**",
        "⚠️ **Spin & Selectivity**",
        "📄 **Editorial Report**"
    ])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
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
                st.error("❌ **Grade: Poor**")
        
        with col2:
            st.markdown("### Critical Issues")
            critical_count = len(results["critical_gaps"])
            if critical_count == 0:
                st.success(f"🎉 No critical reporting issues")
            else:
                st.error(f"🔴 {critical_count} critical issue(s)")
        
        with col3:
            st.markdown("### Spin Detected")
            if results["spin_detected"]:
                st.error("⚠️ Yes - Overinterpretation detected")
            else:
                st.success("✅ No spin detected")
        
        st.markdown("### Reporting Component Scores")
        for component, comp_score in results["section_scores"].items():
            col1, col2 = st.columns([1.5, 3])
            with col1:
                st.write(component.replace("_", " ").title())
            with col2:
                st.progress(comp_score, text=f"{comp_score:.1%}")
    
    with tab2:
        st.markdown("### ✅ Reporting Strengths")
        if results["strengths"]:
            for strength in results["strengths"][:6]:
                st.success(strength)
        else:
            st.info("No specific reporting strengths identified")
        
        st.markdown("### ⚠️ Reporting Issues by Severity")
        
        critical = [i for i in results["issues"] if i.severity == "critical"]
        major = [i for i in results["issues"] if i.severity == "major"]
        
        if critical:
            st.markdown("#### 🔴 Critical Issues (Must Address)")
            for issue in critical:
                with st.expander(f"❌ {issue.description}"):
                    st.write(f"**Location:** {issue.location}")
                    st.write(f"**Recommendation:** {issue.recommendation}")
                    st.write(f"**Best Practice:** {issue.best_practice}")
        
        if major:
            st.markdown("#### 🟠 Major Issues")
            for issue in major[:5]:
                with st.expander(f"⚠️ {issue.description}"):
                    st.write(f"**Recommendation:** {issue.recommendation}")
        
        if results["inconsistencies"]:
            st.markdown("### 🔄 Detected Inconsistencies")
            for inconsistency in results["inconsistencies"]:
                st.warning(inconsistency)
    
    with tab3:
        st.markdown("### 🎯 Selective Reporting Indicators")
        if results["selective_reporting_indicators"]:
            for indicator in results["selective_reporting_indicators"]:
                st.error(f"⚠️ {indicator}")
        else:
            st.success("✅ No selective reporting indicators detected")
        
        st.markdown("### 🧠 Spin Analysis")
        if results["spin_detected"]:
            st.error("**Spin detected in results interpretation**")
            st.markdown("""
            The results section contains language that may overinterpret findings:
            
            - Avoid describing non-significant results as "trending toward significance"
            - Do not use "borderline significant" for p > 0.05
            - Present results objectively without emphasizing numerical differences that lack statistical support
            - Clearly distinguish between primary and exploratory/post-hoc analyses
            """)
        else:
            st.success("**No spin detected** - Results appear to be presented objectively")
        
        st.markdown("### 📋 Reporting Checklist")
        
        checklist_items = {
            "Primary outcomes reported": any("primary" in str(s).lower() for s in results["strengths"]),
            "Secondary outcomes reported": results["section_scores"].get("completeness", 0) > 0.5,
            "Negative results reported": not any("negative" in str(i).lower() for i in results["issues"]),
            "Effect sizes included": any("effect" in str(s).lower() for s in results["strengths"]),
            "Confidence intervals included": any("confidence" in str(s).lower() for s in results["strengths"]),
            "No selective reporting": len(results["selective_reporting_indicators"]) == 0,
            "No spin detected": not results["spin_detected"]
        }
        
        for item, completed in checklist_items.items():
            if completed:
                st.success(f"✅ {item}")
            else:
                st.warning(f"❌ {item}")
    
    with tab4:
        st.markdown("### 📄 Complete Results Reporting Report")
        st.markdown("---")
        st.markdown(results["results_report"])
        
        # Download button
        st.download_button(
            label="📥 Download Results Reporting Report",
            data=results["results_report"],
            file_name=f"results_reporting_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Statistics Review", use_container_width=True):
            st.session_state.page = 4
            st.rerun()
    with col2:
        if st.button("Proceed to Final Summary →", type="primary", use_container_width=True):
            st.session_state.page = 6
            st.rerun()