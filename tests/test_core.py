#!/usr/bin/env python3
"""
Test script for SAVEPIPE package
Contains usage examples and test cases for pipe thickness analysis
"""

from savepipe.core import SAVEPIPE

def test_basic_analysis():
    """Test basic pipe thickness analysis"""
    print("=== Basic Analysis Test ===")
    
    # Create a pipe instance
    pipe = SAVEPIPE(
        schedule="40", 
        nps="2", 
        pressure=50.0, 
        pressure_class=150, 
        metallurgy="CS A106 GR B"
    )
    
    # Perform analysis
    results = pipe.analyze_pipe_thickness(actual_thickness=0.060)
    
    print("Analysis Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")
    
    return pipe, results

def test_report_generation():
    """Test report and visualization generation"""
    print("\n=== Report Generation Test ===")
    
    # Create pipe instance
    pipe = SAVEPIPE(
        schedule="40", 
        nps="2", 
        pressure=50.0, 
        pressure_class=150, 
        metallurgy="CS A106 GR B"
    )
    
    # Generate full report with visualizations
    print("Generating full report and visualizations...")
    report_files = pipe.generate_full_report(actual_thickness=0.060)
    
    print("\nGenerated files:")
    for file_type, filepath in report_files.items():
        if file_type != "analysis_results":
            print(f"  {file_type}: {filepath}")
    
    return report_files

# def test_different_scenarios():
#     """Test different pipe scenarios"""
#     print("\n=== Different Scenarios Test ===")
    
#     scenarios = [
#         {
#             "name": "High Pressure Pipe",
#             "params": {
#                 "schedule": "80",
#                 "nps": "3",
#                 "pressure": 1000.0,
#                 "pressure_class": 1500,
#                 "metallurgy": "CS A106 GR B"
#             },
#             "actual_thickness": 0.200
#         },
#         {
#             "name": "Low Pressure Pipe",
#             "params": {
#                 "schedule": "10",
#                 "nps": "1",
#                 "pressure": 100.0,
#                 "pressure_class": 150,
#                 "metallurgy": "CS A106 GR B"
#             },
#             "actual_thickness": 0.050
#         },
#         {
#             "name": "Critical Pipe (Below Limits)",
#             "params": {
#                 "schedule": "40",
#                 "nps": "4",
#                 "pressure": 800.0,
#                 "pressure_class": 900,
#                 "metallurgy": "CS A106 GR B"
#             },
#             "actual_thickness": 0.050  # Very thin - should trigger warnings
#         }
#     ]
    
#     for scenario in scenarios:
#         print(f"\n--- {scenario['name']} ---")
        
#         # Create pipe instance
#         pipe = SAVEPIPE(**scenario["params"])
        
#         # Perform analysis
#         results = pipe.analyze_pipe_thickness(scenario["actual_thickness"])
        
#         # Print key results
#         print(f"  Limiting Factor: {results['limiting_type']}")
#         print(f"  Limiting Thickness: {results['limiting_thickness']:.4f} inches")
#         print(f"  Actual vs Limiting: {scenario['actual_thickness']:.4f} vs {results['limiting_thickness']:.4f}")
        
#         # Check if adequate
#         if scenario['actual_thickness'] >= results['limiting_thickness']:
#             print("  Status: ADEQUATE")
#         else:
#             print("  Status: INADEQUATE")

# def test_with_corrosion_rate():
#     """Test analysis with corrosion rate for life span calculation"""
#     print("\n=== Corrosion Rate Test ===")
    
#     # Create pipe with corrosion rate
#     pipe = SAVEPIPE(
#         schedule="40", 
#         nps="2", 
#         pressure=500.0, 
#         pressure_class=600, 
#         metallurgy="CS A106 GR B",
#         corrosion_rate=10.0  # 10 mpy corrosion rate
#     )
    
#     # Perform analysis
#     results = pipe.analyze_pipe_thickness(actual_thickness=0.080)
    
#     print("Analysis with Corrosion Rate:")
#     print(f"  Corrosion Rate: {pipe.corrosion_rate} mpy")
#     print(f"  Life Span: {results.get('life_span', 'N/A')} years")
#     print(f"  Above API 574 RL: {results.get('above_api574RL', 'N/A')} inches")

# def test_edge_cases():
#     """Test edge cases and error handling"""
#     print("\n=== Edge Cases Test ===")
    
#     try:
#         # Test with invalid NPS
#         pipe = SAVEPIPE(
#             schedule="40", 
#             nps="999",  # Invalid NPS
#             pressure=500.0, 
#             pressure_class=600, 
#             metallurgy="CS A106 GR B"
#         )
#         results = pipe.analyze_pipe_thickness(actual_thickness=0.060)
#         print("Invalid NPS test completed")
#     except Exception as e:
#         print(f"Invalid NPS test - Expected error: {e}")
    
#     try:
#         # Test with very high pressure
#         pipe = SAVEPIPE(
#             schedule="160", 
#             nps="2", 
#             pressure=5000.0,  # Very high pressure
#             pressure_class=2500, 
#             metallurgy="CS A106 GR B"
#         )
#         results = pipe.analyze_pipe_thickness(actual_thickness=0.200)
#         print(f"High pressure test - Limiting thickness: {results['limiting_thickness']:.4f}")
#     except Exception as e:
#         print(f"High pressure test error: {e}")

def main():
    """Main test function"""
    print("SAVEPIPE TEST SUITE")
    print("=" * 50)
    
    # Run all tests
    test_basic_analysis()
    test_report_generation()
    # test_different_scenarios()
    # test_with_corrosion_rate()
    # test_edge_cases()
    
    print("\n" + "=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    main()
