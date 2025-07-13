import sys
from savepipe.core import SAVEPIPE

def main():
    print("\nSAVEPIPE CLI - Pipe Thickness Analysis\n" + "="*40)
    try:
        schedule = input("Enter pipe schedule (10, 40, 80, 120, 160): ").strip()
        nps = input("Enter nominal pipe size (e.g., 2, 3/4, 1-1/2): ").strip()
        pressure = float(input("Enter design pressure (psi): ").strip())
        pressure_class = int(input("Enter pressure class (150, 300, 600, 900, 1500, 2500): ").strip())
        metallurgy = input("Enter metallurgy (CS A106 GR B, SS 316/316S, SS 304, Inconel 625): ").strip()
        actual_thickness = float(input("Enter actual measured thickness (inches): ").strip())
        corrosion_rate = input("Enter corrosion rate (mpy, optional): ").strip()
        corrosion_rate = float(corrosion_rate) if corrosion_rate else None
    except Exception as e:
        print(f"Input error: {e}")
        sys.exit(1)

    pipe = SAVEPIPE(
        schedule=schedule,
        nps=nps,
        pressure=pressure,
        pressure_class=pressure_class,
        metallurgy=metallurgy,
        corrosion_rate=corrosion_rate
    )

    print("\nRunning analysis...")
    results = pipe.analyze_pipe_thickness(actual_thickness=actual_thickness)
    print("\nAnalysis Results:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    gen_report = input("\nGenerate full report and visualizations? (y/n): ").strip().lower()
    if gen_report == 'y':
        files = pipe.generate_full_report(actual_thickness=actual_thickness)
        print("\nGenerated files:")
        for file_type, filepath in files.items():
            if file_type != "analysis_results":
                print(f"  {file_type}: {filepath}")
        print("\nAll files saved in the Reports/ folder.")
    print("\nDone.")

if __name__ == "__main__":
    main() 