"""
CSV Processor Agent Package

This package provides comprehensive CSV data processing capabilities through
the Google ADK framework. It includes agents and tools for parsing, validating,
analyzing, and transforming CSV data.

Main Components:
- root_agent: Primary CSV processing orchestration agent
- csv_processor_tool: Tool for CSV parsing and validation
- csv_summary_tool: Tool for generating data summaries and statistics

Usage:
    from app.csv_processor import root_agent
    
    # The agent can process CSV strings and provide detailed analysis
"""

from .agent import root_agent, csv_processor_tool, csv_summary_tool

__all__ = ['root_agent', 'csv_processor_tool', 'csv_summary_tool']
