# page4_statistical_analysis_review.py
import streamlit as st
import re
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StatisticalIssue:
    category: str
    severity: str  # critical, major, minor, suggestion
    description: str
    location: str
    recommendation: str
    statistical_concept: str

class DeepStatisticalAnalyzer:
    """Advanced statistical analysis reviewer with comprehensive assessment"""
    
    def __init__(self):
        self.statistical_components = {
            "descriptive_statistics": {
                "weight": 0.20,
                "elements": [
                    "mean_sd_reporting", "median_iqr_reporting", "frequency_percentages",
                    "missing_data_reporting", "baseline_comparisons"
                ]
            },
            "inferential_statistics": {
                "weight": 0.30,
                "elements": [
                    "test_selection_appropriateness", "normality_assessment", "homogeneity_assessment",
                    "parametric_assumptions", "nonparametric_alternatives"
                ]
            },
            "effect_sizes": {
                "weight": 0.15,
                "elements": [
                    "effect_size_reporting", "confidence_intervals", "magnitude_interpretation",
                    "clinical_significance"
                ]
            },
            "advanced_analyses": {
                "weight": 0.20,
                "elements": [
                    "regression_diagnostics", "multiple_testing_correction", "interaction_terms",
                    "sensitivity_analyses", "subgroup_analyses"
                ]
            },
            "software_reproducibility": {
                "weight": 0.15,
                "elements": [
                    "software_specification", "version_reporting", "code_availability",
                    "syntax_reproducibility"
                ]
            }
        }
        
        self.severity_weights = {"critical": 0, "major": 0.5, "minor": 0.75, "suggestion": 0.9}
        
    def analyze(self, text: str, study_design: str = None) -> Dict:
        """Perform comprehensive statistical analysis"""
        
        results = {
            "section_scores": {},
            "overall_score": 0.0,
            "issues": [],
            "strengths": [],
            "critical_gaps": [],
            "p_value_patterns": {},
            "common_errors": [],
            "detailed_feedback": "",
            "statistics_report": ""
        }
        
        # Analyze each component
        for component, config in self.statistical_components.items():
            component_score, component_issues, component_strengths = self._analyze_component(
                text, component, config
            )
            results["section_scores"][component] = component_score
            results["issues"].extend(component_issues)
            results["strengths"].extend(component_strengths)
            results["overall_score"] += component_score * config["weight"]
        
        # Detect p-value patterns
        results["p_value_patterns"] = self._analyze_p_value_patterns(text)
        
        # Identify common statistical errors
        results["common_errors"] = self._identify_common_errors(text)
        
        # Classify critical issues
        results["critical_gaps"] = [i for i in results["issues"] if i.severity == "critical"]
        
        # Generate narrative report
        results["statistics_report"] = self._generate_narrative_report(results)
        
        return results
    
    def _analyze_component(self, text: str, component: str, config: Dict) -> Tuple[float, List, List]:
        """Analyze a specific statistical component"""
        
        element_scores = []
        issues = []
        strengths = []
        
        for element in config["elements"]:
            found, evidence, quality_score = self._check_element(text, element, component)
            
            if found:
                element_scores.append(quality_score)
                if quality_score > 0.7:
                    strengths.append(f"✓ **{self._format_element_name(element)}**: {evidence[:120]}...")
            else:
                severity = "critical" if element in ["test_selection_appropriateness", "effect_size_reporting"] else "major"
                issues.append(StatisticalIssue(
                    category=component,
                    severity=severity,
                    description=f"Missing or inadequate: {self._format_element_name(element)}",
                    location="Results/Statistics section",
                    recommendation=self._get_recommendation(element),
                    statistical_concept=self._get_statistical_concept(element)
                ))
        
        component_score = sum(element_scores) / len(config["elements"]) if element_scores else 0
        return component_score, issues, strengths
    
    def _check_element(self, text: str, element: str, component: str) -> Tuple[bool, str, float]:
        """Check for statistical element presence and quality"""
        
        patterns = {
            "mean_sd_reporting": r"mean[\s\S]{0,30}[±~]\s*\d+\.?\d*|mean\s*\(SD\)",
            "median_iqr_reporting": r"median[\s\S]{0,30}(?:IQR|interquartile|quartile)",
            "frequency_percentages": r"\d+(?:\.\d+)?%|\(n\s*=\s*\d+\)",
            "missing_data_reporting": r"(?:missing data|attrition|dropout|loss to follow-up|complete case|imputation)",
            "test_selection_appropriateness": r"(?:t-test|ANOVA|chi-square|Mann-Whitney|Wilcoxon|Kruskal-Wallis|regression)",
            "normality_assessment": r"(?:Shapiro|Kolmogorov|normality test|normal distribution|Q-Q plot)",
            "homogeneity_assessment": r"(?:Levene|Bartlett|homogeneity of variance|equal variances)",
            "effect_size_reporting": r"(?:effect size|Cohen's d|Hedges' g|eta squared|partial eta|odds ratio|risk ratio)",
            "confidence_intervals": r"(?:CI|confidence interval)\s*[=:]\s*\[?\d+\.?\d*\s*[,–-]\s*\d+\.?\d*\]?",
            "multiple_testing_correction": r"(?:Bonferroni|Holm|FDR|false discovery rate|multiple comparison correction)",
            "regression_diagnostics": r"(?:VIF|tolerance|multicollinearity|residual|goodness-of-fit|Hosmer-Lemeshow)",
            "software_specification": r"(?:SPSS|R|Stata|SAS|Python|JMP|GraphPad|Prism|S-Plus|MATLAB)",
        }
        
        if element in patterns:
            match = re.search(patterns[element], text, re.I)
            if match:
                # Extract context
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                context = text[start:end].strip()
                
                # Assess quality
                quality_score = self._assess_quality(context, element)
                return True, context, quality_score
        
        return False, "", 0.0
    
    def _assess_quality(self, context: str, element: str) -> float:
        """Assess quality of statistical reporting"""
        score = 0.7
        
        # Specific quality indicators
        if element == "effect_size_reporting":
            if re.search(r"\d+\.?\d*\s*\([\d\.\s,]+\)", context):  # With CI
                score += 0.2
            if re.search(r"(?:small|medium|large|negligible)", context, re.I):
                score += 0.1
        elif element == "confidence_intervals":
            if re.search(r"\d+\.?\d*\s*\([\d\.\s,-]+\)", context):
                score += 0.2
        elif element == "test_selection_appropriateness":
            if re.search(r"(?:assumption|appropriate|justified)", context, re.I):
                score += 0.15
        
        # General quality checks
        if re.search(r"\d+", context):
            score += 0.05
        if len(context.split()) > 30:
            score += 0.05
        
        return min(1.0, score)
    
    def _analyze_p_value_patterns(self, text: str) -> Dict:
        """Analyze p-value reporting patterns"""
        patterns = {
            "exact_p_values": len(re.findall(r"p\s*=\s*0\.\d{3,4}", text, re.I)),
            "inequality_p_values": len(re.findall(r"p\s*[<>=]\s*0\.0+1", text, re.I)),
            "trend_p_values": len(re.findall(r"p\s*[<>=]\s*0\.0[5-9]|p\s*=\s*0\.0[5-9]", text, re.I)),
            "non_significant": len(re.findall(r"p\s*[>≥]\s*0\.0[5-9]|not significant|non-significant", text, re.I)),
        }
        
        # Check for p-value precision issues
        patterns["excessive_precision"] = len(re.findall(r"p\s*=\s*0\.\d{5,}", text, re.I))
        
        return patterns
    
    def _identify_common_errors(self, text: str) -> List[str]:
        """Identify common statistical errors in reporting"""
        errors = []
        
        # Error 1: P-value misinterpretation
        if re.search(r"p\s*[<>=]\s*0\.0[0-9]{1,2}[\s\S]{0,100}(?:no difference|no effect|equal)", text, re.I):
            errors.append("Potential p-value misinterpretation: Non-significant p-value does not prove no difference")
        
        # Error 2: Missing effect sizes
        if re.search(r"p\s*[<>=]\s*0\.0[0-9]{1,2}", text, re.I) and not re.search(r"effect size|cohen|eta|odds ratio", text, re.I):
            errors.append("Missing effect sizes: Report effect sizes alongside p-values for meaningful interpretation")
        
        # Error 3: Small sample with parametric tests
        if re.search(r"n\s*[<=]\s*30", text, re.I) and re.search(r"t-test|ANOVA|Pearson", text, re.I):
            errors.append("Potential parametric test misuse: Consider non-parametric alternatives with small samples (n<30)")
        
        # Error 4: Multiple testing without correction
        if re.search(r"(?:multiple|several|many)\s+(?:tests?|comparisons)", text, re.I):
            if not re.search(r"Bonferroni|Holm|FDR|correction", text, re.I):
                errors.append("Multiple testing without correction: Apply multiple comparison corrections to control Type I error")
        
        # Error 5: Overinterpretation of near-significant p-values
        if re.search(r"p\s*=\s*0\.0[5-9][0-9]?[\s\S]{0,100}(?:trend|borderline|close to)", text, re.I):
            errors.append("Overinterpretation of near-significant p-values: p>0.05 indicates non-significance")
        
        return errors
    
    def _format_element_name(self, element: str) -> str:
        """Format element name for display"""
        return element.replace("_", " ").title()
    
    def _get_recommendation(self, element: str) -> str:
        """Generate specific statistical recommendation"""
        recommendations = {
            "mean_sd_reporting": "Report means with standard deviations (Mean ± SD) for normally distributed data",
            "median_iqr_reporting": "Report medians with interquartile ranges (Median [IQR]) for non-normally distributed data",
            "effect_size_reporting": "Report effect sizes (Cohen's d, η², odds ratios) with 95% confidence intervals for all primary outcomes",
            "confidence_intervals": "Include 95% confidence intervals alongside all point estimates",
            "multiple_testing_correction": "Apply and report multiple comparison corrections (Bonferroni, Holm, or FDR)",
            "normality_assessment": "Test and report normality assumptions using Shapiro-Wilk or Kolmogorov-Smirnov tests",
            "missing_data_reporting": "Report missing data frequency and handling method (complete case, imputation, or sensitivity analysis)"
        }
        return recommendations.get(element, f"Provide comprehensive {self._format_element_name(element)}")
    
    def _get_statistical_concept(self, element: str) -> str:
        """Get statistical concept explanation"""
        concepts = {
            "effect_size_reporting": "Effect sizes quantify the magnitude of an effect, independent of sample size",
            "confidence_intervals": "Confidence intervals provide a range of plausible values for population parameters",
            "multiple_testing_correction": "Multiple comparison corrections reduce Type I error inflation from repeated testing"
        }
        return concepts.get(element, "Statistical best practice")
    
    def _generate_narrative_report(self, results: Dict) -> str:
        """Generate comprehensive statistical review report"""
        
        report_lines = []
        report_lines.append("=" * 75)
        report_lines.append("STATISTICAL ANALYSIS REVIEW REPORT")
        report_lines.append("=" * 75)
        report_lines.append("")
        
        # Overall assessment
        overall_score = results["overall_score"]
        if overall_score >= 0.8:
            grade = "EXCELLENT"
            assessment = "Statistical methods are appropriate, well-described, and correctly applied."
        elif overall_score >= 0.7:
            grade = "GOOD"
            assessment = "Statistical methods are largely appropriate with minor deficiencies."
        elif overall_score >= 0.6:
            grade = "FAIR"
            assessment = "Statistical methods have notable gaps requiring moderate revision."
        elif overall_score >= 0.5:
            grade = "POOR"
            assessment = "Statistical methods have major deficiencies requiring substantial revision."
        else:
            grade = "VERY POOR"
            assessment = "Statistical methods are critically flawed and may invalidate findings."
        
        report_lines.append(f"OVERALL STATISTICAL GRADE: {grade}")
        report_lines.append(f"QUALITY SCORE: {overall_score:.1%}")
        report_lines.append("")
        report_lines.append(f"ASSESSMENT: {assessment}")
        report_lines.append("")
        
        # Component scores
        report_lines.append("-" * 50)
        report_lines.append("STATISTICAL COMPONENT SCORES")
        report_lines.append("-" * 50)
        for component, score in results["section_scores"].items():
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            component_name = component.replace("_", " ").title()
            report_lines.append(f"{component_name:25} {bar} {score:.1%}")
        report_lines.append("")
        
        # P-value analysis
        if results["p_value_patterns"]:
            report_lines.append("-" * 50)
            report_lines.append("P-VALUE REPORTING ANALYSIS")
            report_lines.append("-" * 50)
            patterns = results["p_value_patterns"]
            report_lines.append(f"• Exact p-values reported: {patterns['exact_p_values']}")
            report_lines.append(f"• Inequality p-values (p<0.001 etc.): {patterns['inequality_p_values']}")
            report_lines.append(f"• Trend/borderline p-values: {patterns['trend_p_values']}")
            if patterns['excessive_precision'] > 0:
                report_lines.append(f"⚠️ Excessive precision detected: {patterns['excessive_precision']} p-values with >4 decimal places")
            report_lines.append("")
        
        # Common errors identified
        if results["common_errors"]:
            report_lines.append("-" * 50)
            report_lines.append("IDENTIFIED STATISTICAL ERRORS")
            report_lines.append("-" * 50)
            for error in results["common_errors"]:
                report_lines.append(f"⚠️ {error}")
            report_lines.append("")
        
        # Strengths
        if results["strengths"]:
            report_lines.append("-" * 50)
            report_lines.append("STATISTICAL STRENGTHS")
            report_lines.append("-" * 50)
            for strength in results["strengths"][:5]:
                report_lines.append(strength)
            report_lines.append("")
        
        # Critical issues
        critical_issues = [i for i in results["issues"] if i.severity == "critical"]
        if critical_issues:
            report_lines.append("-" * 50)
            report_lines.append("CRITICAL STATISTICAL ISSUES")
            report_lines.append("-" * 50)
            for issue in critical_issues:
                report_lines.append(f"🔴 {issue.description}")
                report_lines.append(f"   → Recommendation: {issue.recommendation}")
                report_lines.append(f"   → Concept: {issue.statistical_concept}")
                report_lines.append("")
        
        # Major issues
        major_issues = [i for i in results["issues"] if i.severity == "major"]
        if major_issues:
            report_lines.append("-" * 50)
            report_lines.append("MAJOR STATISTICAL ISSUES")
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
            report_lines.append(f"1. Address {len(critical_issues)} critical statistical issues before acceptance")
        if results["common_errors"]:
            report_lines.append(f"2. Correct {len(results['common_errors'])} identified statistical errors")
        if results["p_value_patterns"]["exact_p_values"] == 0:
            report_lines.append("3. Report exact p-values (e.g., p=0.034) rather than inequalities when possible")
        if not any("effect_size" in issue.description.lower() for issue in results["issues"]):
            report_lines.append("4. Include effect sizes with confidence intervals for all primary analyses")
        
        report_lines.append("5. Consider statistical consulting for complex analyses or when assumptions are violated")
        report_lines.append("")
        
        report_lines.append("=" * 75)
        report_lines.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 75)
        
        return "\n".join(report_lines)

def show():
    st.markdown("## 📈 **Comprehensive Statistical Analysis Review**")
    
    if "raw_text" not in st.session_state:
        st.error("❌ No manuscript loaded. Please return to upload page.")
        if st.button("← Return to Upload"):
            st.session_state.page = 1
            st.rerun()
        return
    
    text = st.session_state.raw_text
    
    # Get study design from session or detect
    study_design = st.session_state.get("detected_design", None)
    
    # Initialize and run analyzer
    analyzer = DeepStatisticalAnalyzer()
    
    with st.spinner("🔬 Performing comprehensive statistical analysis... This may take a moment"):
        results = analyzer.analyze(text, study_design)
        st.session_state.statistics_results = results
    
    # Display results in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 **Executive Summary**",
        "🔬 **Statistical Findings**",
        "⚠️ **Errors & Issues**",
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
                st.success(f"🎉 No critical statistical issues")
            else:
                st.error(f"🔴 {critical_count} critical issue(s)")
        
        with col3:
            st.markdown("### Common Errors")
            error_count = len(results["common_errors"])
            if error_count == 0:
                st.success("✅ No common errors detected")
            else:
                st.warning(f"⚠️ {error_count} potential error(s)")
        
        st.markdown("### Statistical Component Scores")
        for component, comp_score in results["section_scores"].items():
            col1, col2 = st.columns([1.5, 3])
            with col1:
                st.write(component.replace("_", " ").title())
            with col2:
                st.progress(comp_score, text=f"{comp_score:.1%}")
    
    with tab2:
        st.markdown("### 📊 P-Value Reporting Analysis")
        
        pv = results["p_value_patterns"]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Exact p-values", pv["exact_p_values"])
        with col2:
            st.metric("Inequality p-values", pv["inequality_p_values"])
        with col3:
            st.metric("Non-significant", pv["non_significant"])
        
        if pv["exact_p_values"] > 0:
            st.info("✅ Exact p-values facilitate meta-analysis and precise interpretation")
        if pv["excessive_precision"] > 0:
            st.warning(f"⚠️ {pv['excessive_precision']} p-value(s) reported with excessive precision (5+ decimals)")
        
        st.markdown("### ✅ Statistical Strengths")
        if results["strengths"]:
            for strength in results["strengths"][:6]:
                st.success(strength)
        else:
            st.info("No specific statistical strengths identified")
        
        st.markdown("### 🔬 Effect Size & CI Reporting")
        if any("effect_size_reporting" in str(s) for s in results["strengths"]):
            st.success("Effect sizes are reported - good for clinical interpretation")
        else:
            st.warning("Effect sizes not adequately reported - consider adding for all primary outcomes")
        
        if any("confidence_intervals" in str(s) for s in results["strengths"]):
            st.success("Confidence intervals are reported - good for precision estimation")
        else:
            st.warning("Confidence intervals not systematically reported")
    
    with tab3:
        if results["common_errors"]:
            st.markdown("### 🔴 Identified Statistical Errors")
            for i, error in enumerate(results["common_errors"], 1):
                with st.expander(f"Error {i}: {error[:80]}..."):
                    st.error(error)
                    if "p-value" in error.lower():
                        st.info("💡 **Clarification:** Statistical significance does not imply clinical importance")
                    elif "effect size" in error.lower():
                        st.info("💡 **Recommendation:** Report Cohen's d for t-tests, η² for ANOVA, odds ratios for logistic regression")
        else:
            st.success("✅ No common statistical errors detected")
        
        st.markdown("### ⚠️ Statistical Issues by Severity")
        
        critical = [i for i in results["issues"] if i.severity == "critical"]
        major = [i for i in results["issues"] if i.severity == "major"]
        
        if critical:
            st.markdown("#### 🔴 Critical Issues")
            for issue in critical:
                with st.expander(f"❌ {issue.description}"):
                    st.write(f"**Recommendation:** {issue.recommendation}")
                    st.write(f"**Statistical Concept:** {issue.statistical_concept}")
        
        if major:
            st.markdown("#### 🟠 Major Issues")
            for issue in major[:5]:
                with st.expander(f"⚠️ {issue.description}"):
                    st.write(f"**Recommendation:** {issue.recommendation}")
    
    with tab4:
        st.markdown("### 📄 Complete Statistical Review Report")
        st.markdown("---")
        st.markdown(results["statistics_report"])
        
        # Download button
        st.download_button(
            label="📥 Download Statistical Analysis Report",
            data=results["statistics_report"],
            file_name=f"statistical_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Methodology Review", use_container_width=True):
            st.session_state.page = 3
            st.rerun()
    with col2:
        if st.button("Proceed to Results Reporting Review →", type="primary", use_container_width=True):
            st.session_state.page = 5
            st.rerun()