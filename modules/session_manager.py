# modules/session_manager.py
"""
Session management utilities for MERIT platform
"""

import streamlit as st
from typing import Any, Optional

class SessionManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def initialize_session():
        """Initialize all session variables"""
        defaults = {
            "page": 1,
            "raw_text": "",
            "filename": "",
            "file_uploaded": False,
            "selected_guidelines": [],
            "methodology_results": None,
            "statistics_results": None,
            "results_reporting_results": None,
            "review_depth": "Detailed",
            "critical_focus": [],
            "detected_design": None
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def reset_session():
        """Reset all session variables"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        SessionManager.initialize_session()
    
    @staticmethod
    def get_session_var(key: str, default: Any = None) -> Any:
        """Get session variable safely"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set_session_var(key: str, value: Any):
        """Set session variable"""
        st.session_state[key] = value