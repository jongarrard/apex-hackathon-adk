"""
CSV Processing Agent for data transformation and analysis.

This agent provides comprehensive CSV data processing capabilities including
parsing, validation, transformation, and analysis. It serves as the orchestration
layer for CSV data workflows, handling file input, processing coordination,
and result delivery.
"""

import pandas as pd
from typing import Dict, Any, List, Optional
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext


def process_csv_data(csv_string: str) -> Dict[str, Any]:
    """
    Process CSV string data and perform initial validation and parsing.
    
    This function serves as the primary entry point for CSV data processing.
    It handles CSV parsing, validates data structure, and prepares the data
    for subsequent transformation operations.
    
    Args:
        csv_string (str): Raw CSV data as a string containing headers and data rows.
                         Must be properly formatted CSV with comma-separated values.
    
    Returns:
        Dict[str, Any]: Processing result containing:
            - success (bool): Whether processing completed successfully
            - data_info (Dict): Metadata about the processed CSV including:
                - row_count (int): Number of data rows (excluding header)
                - column_count (int): Number of columns
                - columns (List[str]): Column names from header
                - data_types (Dict[str, str]): Inferred data types per column
            - preview (List[Dict]): First 5 rows of data as list of dictionaries
            - errors (List[str]): Any validation errors or warnings encountered
    
    Raises:
        ValueError: When CSV string is empty, malformed, or contains invalid data
        pandas.errors.ParserError: When CSV parsing fails due to format issues
        Exception: For unexpected processing errors with detailed error context
    
    Examples:
        >>> csv_data = "name,age,city\\nJohn,25,NYC\\nJane,30,LA"
        >>> result = process_csv_data(csv_data)
        >>> print(result['data_info']['row_count'])  # Output: 2
        >>> print(result['data_info']['columns'])    # Output: ['name', 'age', 'city']
    """
    try:
        # Validate input
        if not csv_string or not csv_string.strip():
            raise ValueError("CSV string cannot be empty")
        
        # Parse CSV data using pandas
        from io import StringIO
        csv_buffer = StringIO(csv_string)
        df = pd.read_csv(csv_buffer)
        
        # Validate parsed data
        if df.empty:
            raise ValueError("CSV contains no data rows")
        data_info = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'data_types': {col: str(df[col].dtype) for col in df.columns}
        }
        preview = df.head(5).to_dict(orient='records')
        # --- Canonical header mapping logic ---
        # List of canonical headers and their normalized forms
        canonical_headers = [
            "Status",
            "Employee #",
            "First Name",
            "Preferred Name",
            "Middle Name",
            "Last Name",
            "Birth Date",
            "SSN",
            "NIN",
            "Gender",
            "Marital Status",
            "Address Line 1",
            "Address Line 2",
            "City",
            "State",
            "ZIP Code",
            "Country",
            "Mobile Phone",
            "Home Phone",
            "Work Phone",
            "Work Ext.",
            "Work Email",
            "Home Email",
            "Hire Date",
            "Ethnicity",
            "EEO Job Category",
            "Veteran Status",
            "Nationality",
            "Partner Specific Employee ID",
            "Standard Hours Per Week",
            "Title",
            "Address"
        ]
        # Helper: normalize header for fuzzy matching
        def normalize(header: str) -> str:
            return header.strip().lower().replace("#", "number").replace(".", "").replace("_", " ").replace("-", " ").replace("/", " ").replace("  ", " ")
        # Build mapping from normalized canonical header to canonical header
        canonical_map = {normalize(h): h for h in canonical_headers}
        # Normalize CSV headers
        csv_headers = list(df.columns)
        normalized_csv_headers = {normalize(h): h for h in csv_headers}
        # Attempt to match CSV headers to canonical headers (case-insensitive, flexible)
        header_matches = {}
        for n_csv, orig_csv in normalized_csv_headers.items():
            for n_canon, canon in canonical_map.items():
                # Simple substring or exact match
                if n_canon == n_csv or n_canon in n_csv or n_csv in n_canon:
                    header_matches[orig_csv] = canon
                    break
        # For each row, build the mapping output
        header_mappings = []
        for _, row in df.iterrows():
            for csv_header, canon_header in header_matches.items():
                value = row[csv_header]
                header_mappings.append({
                    "new_header": canon_header,
                    "old_header": csv_header,
                    "value": value
                })
        return {
            'success': True,
            'data_info': data_info,
            'preview': preview,
            'errors': [],
            'message': f"Successfully processed CSV with {len(df)} rows and {len(df.columns)} columns",
            'header_mappings': header_mappings
        }
    except pd.errors.ParserError as e:
        error_msg = f"CSV parsing error: {str(e)}"
        return {
            'success': False,
            'data_info': {},
            'preview': [],
            'errors': [error_msg],
            'message': error_msg
        }
    except ValueError as e:
        error_msg = f"CSV validation failed: {str(e)}"
        return {
            'success': False,
            'data_info': {},
            'preview': [],
            'errors': [error_msg],
            'message': error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error processing CSV: {str(e)}"
        return {
            'success': False,
            'data_info': {},
            'preview': [],
            'errors': [error_msg],
            'message': error_msg
        }


def get_csv_summary(csv_string: str) -> Dict[str, Any]:
    """
    Generate comprehensive summary statistics for processed CSV data.
    
    Parses the provided CSV string and provides detailed statistical
    summary including descriptive statistics, data distribution insights,
    and data quality metrics.
    
    Args:
        csv_string (str): Raw CSV data as a string containing headers and data rows.
                         Must be properly formatted CSV with comma-separated values.
    
    Returns:
        Dict[str, Any]: Summary statistics containing:
            - success (bool): Whether summary generation completed successfully
            - numeric_summary (Dict): Descriptive statistics for numeric columns
            - categorical_summary (Dict): Value counts for categorical columns
            - data_quality (Dict): Data quality metrics and insights
            - recommendations (List[str]): Suggested data improvements or transformations
            - message (str): Human-readable summary of the result
    
    Raises:
        ValueError: When CSV data is invalid or cannot be parsed
        Exception: For unexpected analysis errors with detailed error context
    """
    import pandas as pd
    from io import StringIO
    try:
        df = pd.read_csv(StringIO(csv_string))
        if df.empty:
            raise ValueError("CSV contains no data rows")

        # Numeric summary
        numeric_cols = df.select_dtypes(include=['number']).columns
        numeric_summary = {}
        if len(numeric_cols) > 0:
            numeric_summary = df[numeric_cols].describe().to_dict()

        # Categorical summary
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_summary = {}
        for col in categorical_cols:
            categorical_summary[col] = df[col].value_counts(dropna=False).to_dict()

        # Data quality metrics
        missing_counts = df.isnull().sum().to_dict()
        duplicate_count = int(df.duplicated().sum())
        data_quality = {
            'missing_values': missing_counts,
            'duplicate_rows': duplicate_count
        }

        # Recommendations
        recommendations = []
        for col, count in missing_counts.items():
            if count > 0:
                recommendations.append(f"Column '{col}' has {count} missing values.")
        if duplicate_count > 0:
            recommendations.append(f"Found {duplicate_count} duplicate rows.")
        if not recommendations:
            recommendations.append("No major data quality issues detected.")

        return {
            'success': True,
            'numeric_summary': numeric_summary,
            'categorical_summary': categorical_summary,
            'data_quality': data_quality,
            'recommendations': recommendations,
            'message': f"Summary generated for {len(df)} rows and {len(df.columns)} columns."
        }
    except pd.errors.ParserError as e:
        error_msg = f"CSV parsing error: {str(e)}"
        return {
            'success': False,
            'numeric_summary': {},
            'categorical_summary': {},
            'data_quality': {},
            'recommendations': [],
            'message': error_msg
        }
    except ValueError as e:
        error_msg = f"CSV validation failed: {str(e)}"
        return {
            'success': False,
            'numeric_summary': {},
            'categorical_summary': {},
            'data_quality': {},
            'recommendations': [],
            'message': error_msg
        }
    except Exception as e:
        error_msg = f"Error generating CSV summary: {str(e)}"
        return {
            'success': False,
            'numeric_summary': {},
            'categorical_summary': {},
            'data_quality': {},
            'recommendations': [],
            'message': error_msg
        }


# Create FunctionTools for CSV processing
csv_processor_tool = FunctionTool(process_csv_data)
csv_summary_tool = FunctionTool(get_csv_summary)

# Define the root CSV processing agent
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="csv_processor_agent",
    description="""
    Advanced CSV Processing Agent for data transformation and analysis workflows.
    
    This agent specializes in comprehensive CSV data processing, providing capabilities for:
    - CSV parsing and validation with detailed error handling
    - Data quality assessment and statistical analysis
    - Extensible transformation pipeline preparation
    - Inter-agent data sharing through context state management
    
    The agent serves as the orchestration hub for CSV-related operations, coordinating
    between data input, processing, validation, and transformation stages. It maintains
    data state across processing steps and provides detailed feedback on data quality
    and structure.
    
    Key capabilities:
    - Robust CSV parsing with pandas integration
    - Comprehensive data validation and quality checks
    - Statistical summary generation for numeric and categorical data
    - Error handling with detailed diagnostic information
    - State management for multi-step processing workflows
    """,
    instruction="""
    You are a specialized CSV processing agent designed to handle data transformation workflows.
    
    Your primary responsibilities:
    1. Accept CSV string data and perform thorough parsing and validation
    2. Analyze data structure, types, and quality metrics
    3. Generate comprehensive summaries and insights about the dataset
    4. Prepare data for subsequent transformation operations
    5. Provide clear feedback on data issues and recommendations
    
    When processing CSV data:
    - Always validate input format and structure first
    - Provide detailed information about columns, data types, and row counts
    - Identify and report data quality issues (missing values, duplicates, etc.)
    - Generate meaningful previews and summaries
    - Store processed data in context for other agents to access
    - Offer actionable recommendations for data improvement
    
    Be thorough in your analysis but concise in your communication. Focus on providing
    actionable insights that help users understand their data and make informed decisions
    about transformations.
    """,
    tools=[csv_processor_tool, csv_summary_tool]
)
