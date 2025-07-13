# SAVEPIPE - Still under development
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

These aren't theoretical questions - they're real decisions that affect production, safety, and the bottom line. SAVEPIPE was built by engineers, for engineers, to provide the analytical rigor needed for these critical decisions.

## Understanding Pipe Retirement Limits

Imagine a pipe wall gradually thinning over a 10-year span, slowly approaching a critical red line - the **retirement limit**. This is the minimum acceptable wall thickness that ensures safe operation. When the actual thickness hits this line, the pipe must be retired or replaced immediately.

### The Two Minimum Thickness Requirements

Pipe design involves two distinct minimum thickness calculations. The **pressure design minimum** ensures the pipe can contain internal pressure safely using ASME B31.1 equations that consider design pressure, temperature effects, and material properties. The **structural minimum** ensures the pipe can support its own weight and external loads according to API 574 Table D.2 requirements, which becomes critical for per-code pipe spans. However, this package does not account for fluid weight, insulation, heat tracing equipment, pipe hangers, and other per-application basis.

The **limiting thickness** is whichever of these two values is more restrictive. SAVEPIPE automatically determines which factor controls your design and provides clear guidance on current status, remaining life, and required actions.

### Corrosion Allowance and Remaining Life

The difference between your actual thickness and the retirement limit is your **corrosion allowance** - essentially your safety margin. This allowance, combined with your known corrosion rate from inspection reports, determines how much time you have before retirement becomes mandatory. 

This analytical approach transforms the complex retirement decision into a clear, data-driven process that balances operational needs with safety requirements.




## Overview

SAVEPIPE is a sophisticated pipe thickness analysis tool designed for mechanical integrity engineers, reliability specialists, and operations teams in the oil and gas industry. It provides automated analysis of pipe wall thickness against multiple design criteria and generates professional reports with actionable recommendations.

## Install

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then install SAVEPIPE with pip:

```bash
pip install savepipe
```

---

## Example

### Run as a CLI Tool

```bash
savepipe
```
Follow the prompts to analyze your pipe and generate reports.

### Or Use as a Python API

```python
from savepipe.core import SAVEPIPE

# Create a pipe instance
pipe = SAVEPIPE(
    schedule="40",
    nps="2", 
    pressure=50.0,
    pressure_class=150,
    metallurgy="CS A106 GR B",
    corrosion_rate=10.0  # mpy (optional)
)

# Perform comprehensive analysis
results = pipe.analyze_pipe_thickness(actual_thickness=0.060)

# Generate full report with visualizations
report_files = pipe.generate_full_report(actual_thickness=0.060)
```

### Output Reports and Visuals

An folder called "Reports" will be automatically generated in the user's root directory and populated with .txt reports and helpful visualizations of the SAVEPIPE analysis.

All files are automatically named with timestamps:
```
Reports/
├── 20250712_181928_SAVEPIPE_report_SAVEPIPE_20250712_181928.txt
├── 20250712_181928_SAVEPIPE_summary_20250712_181928.txt
├── 20250712_181928_thickness_analysis_number_line.png
└── 20250712_181928_thickness_comparison_chart.png
```

<img width="3477" height="1649" alt="20250713_165615_thickness_analysis_number_line" src="https://github.com/user-attachments/assets/bf614058-3032-440e-9dae-51471d9d518b" />

The Pipe Wall Profile visual shown above illustrates the actual propertions of actual thicknesses to the nominal pipe wall thickness - making it clear as to how much pipe as erroded and how much pipe remains as well as retirement limit benchmarks along the pipe wall. The Y-axis(x=0) can be interpreted as the original insider diameter of the pipe.

<img width="2968" height="1769" alt="20250713_165615_thickness_comparison_chart" src="https://github.com/user-attachments/assets/1bffe8e2-df37-48bc-afe4-26761c14dc10" />


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
python -m tests.test_core
```

The test suite includes:
- Basic analysis functionality
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

MIT License

## Disclaimer

SAVEPIPE is a decision support tool designed to assist qualified engineers in making informed decisions about pipe integrity. It should be used in conjunction with professional engineering judgment and should not be the sole basis for critical safety decisions. Always consult with qualified personnel and follow applicable codes and standards.

## Contact

For questions, suggestions, or contributions, please contact:

andrew[dot]trepagnier[at]icloud.com

---

**SAVEPIPE** - Making critical infrastructure decisions safer and more informed.



