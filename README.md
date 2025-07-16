# TMIN

The Industry-proven tool for determining retirement limits of process piping.

## Introduction

Many oil and gas companies are faced with maintaining 10,000+ miles of 100+ year old piping networks supporting multi-billion dollar/year processing operations. There is rarely a simple solution to immediately shutdown a process pipe - as these shutdowns more often than not impact other units and cost companies millions in time and resources.

In mechanical integrity engineering, we are frequently asked the hard question - **do we have to shutdown the pipe immediately, or do we have time?** Pipe retirement requires rigorous analysis. You must find the perfect balance - such that one isn't squandering company time/resources but also holding personnel safety paramount.

**This is more than a python package, it is a comprehensive engineering decision support system for critical infrastructure safety and operational continuity.**

## The Challenge

**Cross-section of Pipe Wall Thinning Over Time**

![pipe_thinning](https://github.com/user-attachments/assets/02328bf4-90e7-47f2-aa1b-324c773508dd)

Every day, mechanical integrity engineers face decisions that can cost millions of dollars or risk catastrophic failure. When a pipe shows signs of thinning, the clock starts ticking. You need answers fast:

- **Can this pipe continue operating safely?**
- **How much time do we have before retirement is mandatory?**
- **What are the consequences of immediate shutdown vs. continued operation?**
- **How do we balance operational continuity with personnel safety?**

These aren't theoretical questions - they're real decisions that affect production, safety, and the bottom line. TMIN was built by engineers, for engineers, to provide the analytical rigor needed for these critical decisions.

## Understanding Pipe Retirement Limits

Imagine a pipe wall gradually thinning over a 10-year span, slowly approaching a critical red line - the **retirement limit**. This is the minimum acceptable wall thickness that ensures safe operation. When the actual thickness hits this line, the pipe must be retired or replaced immediately.

### The Two Minimum Thickness Requirements

Pipe design involves two distinct minimum thickness calculations. The **pressure design minimum** ensures the pipe can contain internal pressure safely using ASME B31.1 equations that consider design pressure, temperature effects, and material properties. The **structural minimum** ensures the pipe can support its own weight and external loads according to API 574 Table D.2 requirements, which becomes critical for per-code pipe spans. However, this package does not account for fluid weight, insulation, heat tracing equipment, pipe hangers, and other per-application basis.

The **limiting thickness** is whichever of these two values is more restrictive. TMIN automatically determines which factor controls your design and provides clear guidance on current status, remaining life, and required actions.

### Corrosion Allowance and Remaining Life

The difference between your actual thickness and the retirement limit is your **corrosion allowance** - essentially your safety margin. This allowance, combined with your known corrosion rate from inspection reports, determines how much time you have before retirement becomes mandatory.

This analytical approach transforms the complex retirement decision into a clear, data-driven process that balances operational needs with safety requirements.

## Overview

TMIN is a sophisticated pipe thickness analysis tool designed for mechanical integrity engineers, reliability specialists, and operations teams in the oil and gas industry. It provides automated analysis of pipe wall thickness against multiple design criteria and generates professional reports with actionable recommendations.

## Auto-generated Visualization and Results



## Install

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then install TMIN with pip:

```bash
pip install tmin
```

---

## How It Works: Time-Based Corrosion Adjustment

TMIN allows you to supply both the measured thickness and the year that measurement was taken. If you also provide a corrosion rate (in mpy), TMIN will automatically calculate the present-day (current) thickness by accounting for the metal loss since the last inspection.

**Calculation:**

```
present_day_thickness = measured_thickness - (corrosion_rate × years_elapsed × 0.001)
```
- `measured_thickness`: The thickness measured during the last inspection (inches)
- `corrosion_rate`: Corrosion rate in mils per year (mpy)
- `years_elapsed`: Years since the inspection (current year - inspection year)
- `0.001`: Conversion factor from mpy to inches per year

If you do not supply an inspection year or corrosion rate, TMIN will use the measured thickness as the present-day thickness.

## Example

### Run as a CLI Tool

```bash
tmin
```
Follow the prompts to analyze your pipe and generate reports. You will be asked for:
- Measured thickness during inspection (inches)
- Year when thickness was measured (e.g., 2022)
- Corrosion rate (mpy, optional)

TMIN will calculate the present-day thickness and use it for all analysis and reporting.

### Or Use as a Python API

```python
from tmin.core import PIPE

# Create a pipe instance
pipe = PIPE(
    schedule="40",
    nps="2", 
    pressure=50.0,
    pressure_class=150,
    metallurgy="CS A106 GR B",
    corrosion_rate=10.0  # mpy (optional)
)

# Analyze with time-based corrosion adjustment
results = pipe.analyze_pipe_thickness(measured_thickness=0.060, year_inspected=2023)
print("Present-day thickness:", results["actual_thickness"])

# Generate full report with visualizations
report_files = pipe.generate_full_report(measured_thickness=0.060, year_inspected=2023)
```

### Example Output of Reports and Visuals

A folder called "Reports" will be automatically generated in the user's root directory and populated with .txt reports and helpful visualizations of the TMIN analysis. The report will show both the measured thickness, the inspection year, and the calculated present-day thickness.

### Pressure Design (ASME B31.1)
- Calculates minimum wall thickness for pressure containment
- Considers temperature effects via WSRF (Weld Strength Reduction Factor)
- Uses Y-coefficient for high-temperature applications

### Structural Requirements (API 574)
- Evaluates minimum thickness for structural integrity
- Considers pipe deflection and weight loading
- Based on API 574 Table D.2 requirements

### Retirement Limits
- **API 574 Retirement Limit**: Code-mandated minimum thickness
- **Table 5 Retirement Limit**: Company-specific maintenance limits
- **Custom Limits**: User-defined retirement criteria

### Corrosion Analysis
- **Life Span Prediction**: Based on corrosion rate and thickness excess
- **Corrosion Allowance**: Thickness above retirement limits
- **Monitoring Recommendations**: Inspection frequency guidance

## Output Files

When you run a full analysis, TMIN automatically creates a `Reports/` folder and generates:

### 📄 **Text Reports**
- **Full Report**: Comprehensive analysis with all details and recommendations
- **Summary Report**: Executive summary for management review

### 📊 **Visualizations**
- **Number Line Plot**: Shows all thickness values on a scale for easy comparison
- **Comparison Chart**: Bar chart highlighting the limiting factor

### 📁 **File Naming**
All files are automatically named with timestamps:
```
Reports/
├── 20250712_181928_TMIN_report_TMIN_20250712_181928.txt
├── 20250712_181928_TMIN_summary_20250712_181928.txt
├── 20250712_181928_thickness_analysis_number_line.png
└── 20250712_181928_thickness_comparison_chart.png
```

## Supported Pipe Specifications

### Schedules
- 10, 40, 80, 120, 160

### Nominal Pipe Sizes (NPS)
- 0.5" to 24" (varies by schedule)

### Pressure Classes
- 150, 300, 600, 900, 1500, 2500

### Metallurgies
- CS A106 GR B (Carbon Steel)
- SS 316/316S (Stainless Steel) - Coming Soon
- SS 304 (Stainless Steel) - Coming Soon
- Inconel 625 (Nickel Alloy) - Coming Soon

## Testing

Run the comprehensive test suite:

```bash
python -m pytest tests/test_core.py -v
```

The test suite includes:
- Basic analysis functionality
- Time-based corrosion adjustment
- Report generation
- Multiple pipe scenarios
- Corrosion rate analysis
- Edge case handling

## Contributing

This project is designed for the mechanical integrity engineering community. Contributions are welcome, especially for:

- Additional metallurgy support
- New retirement limit standards
- Enhanced visualization features
- Additional analysis criteria

## License

[Add your license information here]

## Disclaimer

TMIN is a decision support tool designed to assist qualified engineers in making informed decisions about pipe integrity. It should be used in conjunction with professional engineering judgment and should not be the sole basis for critical safety decisions. Always consult with qualified personnel and follow applicable codes and standards.

## Contact

For questions, suggestions, or contributions, please contact andrew[dot]trepagnier[at]icloud.com

---

**TMIN** - Making critical infrastructure decisions safer and more informed.



