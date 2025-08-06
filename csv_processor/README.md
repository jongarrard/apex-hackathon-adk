# CSV Processor Agent

A comprehensive CSV data processing agent built with the Google ADK framework. This agent provides robust CSV parsing, validation, analysis, and preparation for data transformations.

## Agent Capabilities

### Core Functions
- **CSV Parsing & Validation**: Robust parsing of CSV strings with comprehensive error handling
- **Data Quality Assessment**: Identifies missing values, duplicates, and data inconsistencies
- **Statistical Analysis**: Generates descriptive statistics for numeric and categorical columns
- **Data Profiling**: Provides insights into data distribution and structure
- **Transformation Preparation**: Prepares data for subsequent transformation operations

### Key Features
- Pandas-based CSV processing for reliability and performance
- Comprehensive error handling with detailed diagnostic messages
- State management for multi-step processing workflows
- Extensible architecture for adding custom transformations
- Data quality recommendations and actionable insights

## Usage

### Basic CSV Processing
```python
from app.csv_processor import root_agent

# Process a CSV string
csv_data = """name,age,city,salary
John Doe,25,New York,50000
Jane Smith,30,Los Angeles,60000
Bob Johnson,35,Chicago,55000"""

# The agent will parse, validate, and analyze the data
response = root_agent.process(csv_data)
```

### Agent Workflow
1. **Input Validation**: Checks CSV format and structure
2. **Data Parsing**: Uses pandas for robust CSV parsing
3. **Quality Assessment**: Identifies data quality issues
4. **Statistical Analysis**: Generates comprehensive summaries
5. **Recommendations**: Provides actionable improvement suggestions

## Tools Available

### `process_csv_data`
Primary tool for CSV processing and validation.

**Input**: CSV string data
**Output**: 
- Processing success status
- Data metadata (rows, columns, types)
- Data preview (first 5 rows)
- Validation errors and warnings

### `get_csv_summary`
Generates comprehensive statistical summaries.

**Input**: Processed CSV data from context
**Output**:
- Descriptive statistics for numeric columns
- Value distributions for categorical columns
- Data quality metrics
- Improvement recommendations

## Data Quality Checks

The agent performs several data quality assessments:

- **Missing Values**: Identifies and counts null/empty values per column
- **Duplicate Detection**: Finds and reports duplicate rows
- **Data Type Validation**: Infers and validates column data types
- **Structure Validation**: Ensures consistent row/column structure

## Error Handling

Comprehensive error handling covers:
- Malformed CSV format
- Empty or invalid data
- Parsing errors
- Memory limitations
- Unexpected processing errors

## Integration

The agent integrates seamlessly with other ADK agents through:
- **Context State Management**: Shares processed data via ToolContext
- **Standardized Interfaces**: Consistent input/output formats
- **Error Propagation**: Clear error reporting for debugging

## Configuration

Environment variables (see `.env.example`):
- `CSV_PROCESSOR_MODEL`: LLM model for the agent
- `MAX_CSV_SIZE_MB`: Maximum CSV file size limit
- `MAX_ROWS_PREVIEW`: Number of rows in data preview
- `ENABLE_ADVANCED_STATS`: Toggle for advanced statistical analysis

## Future Enhancements

The agent is designed to be extensible for:
- Custom data transformations
- Advanced statistical analysis
- Data visualization generation
- Integration with external data sources
- Machine learning preprocessing

## Examples

### Sample CSV Processing Result
```json
{
  "success": true,
  "data_info": {
    "row_count": 3,
    "column_count": 4,
    "columns": ["name", "age", "city", "salary"],
    "data_types": {
      "name": "object",
      "age": "int64", 
      "city": "object",
      "salary": "int64"
    }
  },
  "preview": [
    {"name": "John Doe", "age": 25, "city": "New York", "salary": 50000}
  ],
  "errors": [],
  "message": "Successfully processed CSV with 3 rows and 4 columns"
}
```

This agent provides a solid foundation for CSV data processing workflows and can be extended with additional transformation capabilities as needed.
