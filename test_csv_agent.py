#!/usr/bin/env python3
"""
Test script for the CSV Processing Agent.

This script demonstrates the CSV processing agent capabilities with sample data
and validates that the agent functions correctly within the Google ADK framework.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.csv_processor import root_agent


def test_csv_processing():
    """Test the CSV processing agent with sample data."""
    
    # Sample CSV data for testing
    sample_csv = """name,age,city,salary,department
John Doe,25,New York,50000,Engineering
Jane Smith,30,Los Angeles,60000,Marketing
Bob Johnson,35,Chicago,55000,Engineering
Alice Brown,28,Boston,52000,Sales
Charlie Wilson,32,Seattle,58000,Engineering
Diana Davis,29,Miami,54000,Marketing
Eve Miller,27,Denver,51000,Sales
Frank Garcia,31,Austin,57000,Engineering
Grace Lee,26,Portland,49000,Marketing
Henry Taylor,33,Phoenix,56000,Sales"""

    print("🚀 Testing CSV Processing Agent")
    print("=" * 50)
    
    print(f"📊 Sample CSV Data ({len(sample_csv.split(chr(10)))-1} rows):")
    print(sample_csv[:200] + "..." if len(sample_csv) > 200 else sample_csv)
    print("\n" + "=" * 50)
    
    try:
        # Test the agent with the sample CSV
        print("🔄 Processing CSV data with agent...")
        
        # Create a prompt for the agent
        prompt = f"""
        Please process this CSV data and provide a comprehensive analysis:
        
        {sample_csv}
        
        I need you to:
        1. Parse and validate the CSV data
        2. Provide data quality assessment
        3. Generate statistical summaries
        4. Give recommendations for any improvements
        """
        
        # Note: In a real implementation, you would use the ADK framework to run the agent
        # For now, we'll test the individual tools directly
        from google.adk.core import ToolContext
        
        # Create a mock context
        context = ToolContext()
        context.state = {}
        
        # Test the CSV processing tool directly
        from app.csv_processor.agent import process_csv_data, get_csv_summary
        
        print("✅ Testing CSV processing tool...")
        result = process_csv_data(sample_csv, context)
        
        if result['success']:
            print(f"✅ CSV Processing Successful!")
            print(f"   📈 Rows: {result['data_info']['row_count']}")
            print(f"   📊 Columns: {result['data_info']['column_count']}")
            print(f"   🏷️  Column Names: {', '.join(result['data_info']['columns'])}")
            print(f"   ⚠️  Errors: {len(result['errors'])}")
            
            if result['errors']:
                print("   🚨 Data Quality Issues:")
                for error in result['errors']:
                    print(f"      - {error}")
            
            print("\n📋 Data Preview:")
            for i, row in enumerate(result['preview'][:3], 1):
                print(f"   Row {i}: {row}")
            
            # Test summary generation
            print("\n🔄 Generating data summary...")
            summary_result = get_csv_summary(context)
            
            if summary_result['success']:
                print("✅ Summary Generation Successful!")
                
                if summary_result['numeric_summary']:
                    print("\n📊 Numeric Columns Summary:")
                    for col, stats in summary_result['numeric_summary'].items():
                        if isinstance(stats, dict) and 'mean' in stats:
                            print(f"   {col}: Mean={stats['mean']:.1f}, Std={stats['std']:.1f}")
                
                if summary_result['categorical_summary']:
                    print("\n🏷️  Categorical Columns Summary:")
                    for col, values in summary_result['categorical_summary'].items():
                        top_value = list(values.keys())[0] if values else "N/A"
                        print(f"   {col}: Most common = '{top_value}' ({values.get(top_value, 0)} times)")
                
                print(f"\n🎯 Data Quality Score:")
                quality = summary_result['data_quality']
                print(f"   📊 Total Cells: {quality['total_cells']}")
                print(f"   ❌ Missing: {quality['missing_cells']} ({quality['missing_percentage']}%)")
                print(f"   🔄 Duplicates: {quality['duplicate_rows']}")
                
                if summary_result['recommendations']:
                    print("\n💡 Recommendations:")
                    for rec in summary_result['recommendations']:
                        print(f"   • {rec}")
            else:
                print(f"❌ Summary generation failed: {summary_result['message']}")
                
        else:
            print(f"❌ CSV Processing Failed: {result['message']}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")


if __name__ == "__main__":
    test_csv_processing()
