from .asmetables.od_table import trueOD_40, trueOD_80, trueOD_10, trueOD_120, trueOD_160
from .asmetables.wsrf import WSRF
from .asmetables.y_coeff import ferritic_steels_y, austenitic_steels_y, other_metals_y, nickel_alloy_N06690_y, nickel_alloys_N06617_N08800_N08810_N08825_y, cast_iron_y
from .asmetables.yield_stress import S_, E_
from .asmetables.api_574 import API574_CS_400F, API574_SS_400F

import numpy as np
from dataclasses import dataclass
from typing import Literal, Optional, Dict
import json
import matplotlib.pyplot as plt
from datetime import datetime

@dataclass
class SAVEPIPE:

    #########################################
    # Initialized Arguments with Typing Hints
    #########################################
    #run: str  
    schedule: str  # Pipe schedule (10, 40, 80, 120, 160)
    nps: str  # Nominal pipe size (e.g., '2', '3/4', '1-1/2')
    pressure: float  # Design pressure (psi)
    pressure_class: Literal[150, 300, 600, 900, 1500, 2500]
    metallurgy: Literal["CS A106 GR B", "SS 316/316S", "SS 304", "Inconel 625"]
    pipe_config: Literal["straight", "bend-90", "bend-45", "tee", "elbow"] = "straight"  # Pipe configuration
    corrosion_rate: Optional[float] = None #mpy 
    default_retirement_limit: Optional[float] = None

    # Valid pipe types for reference
    VALID_PIPE_TYPES = ["straight", "bend-90", "bend-45", "tee", "elbow"]
    
    # Valid schedules for reference
    VALID_SCHEDULES = ["10", "40", "80", "120", "160"]

    # Add the missing attributes that are referenced in methods
    trueOD_10 = trueOD_10
    trueOD_40 = trueOD_40
    trueOD_80 = trueOD_80
    trueOD_120 = trueOD_120
    trueOD_160 = trueOD_160
    WSRF = WSRF
    ferritic_steels_y = ferritic_steels_y
    S_allow = S_
    E_ = E_
    API574_CS_400F = API574_CS_400F
    API574_SS_400F = API574_SS_400F

    #########################
    # Add propreitary JSON file or CSV of retirement limit structural thicknesses below to be considered into the analysis, if not, comment out

    def which_API_table(self) -> float:
        try:
            nps_key = float(self.nps)
        except Exception:
            print(f"Could not convert NPS '{self.nps}' to float for API574 lookup.")
            return None
        
        if self.metallurgy == "CS A106 GR B":
            api574_specified_tmin = API574_CS_400F.get(nps_key, {}).get(self.pressure_class)
            if api574_specified_tmin is None:
                print(f"No API574 value for NPS {nps_key} and class {self.pressure_class}")
            return api574_specified_tmin
        
        elif self.metallurgy == "SS 316/316S":
            api574_specified_tmin = API574_SS_400F
            if api574_specified_tmin is None:
                print(f"No API574 value for NPS {nps_key} and class {self.pressure_class}")
            return api574_specified_tmin
        
        else:
            print("No API574 Table Available for this Metallurgy")
            return None
    

    def allowable(self, Syield) -> float:
        return Syield*(2/3)

    def get_OD(self) -> float:
        """Get outside diameter based on schedule and NPS"""
        if self.schedule == "10":
            return self.trueOD_10.get(self.nps)
        elif self.schedule == "40":
            return self.trueOD_40.get(self.nps)
        elif self.schedule == "80":
            return self.trueOD_80.get(self.nps)
        elif self.schedule == "120":
            return self.trueOD_120.get(self.nps)
        elif self.schedule == "160":
            return self.trueOD_160.get(self.nps)
        else:
            raise ValueError(f"Invalid schedule: {self.schedule}")

    def get_Y_coefficient(self) -> float:
        """Get Y coefficient from ASME B31.1 Table 104.1.2-1"""
        if self.metallurgy =='CS A106 GR B':
            return self.ferritic_steels_y[900]
        elif self.metallurgy =='SS 316/316S':
            return self.austenitic_steels_y[900]
        

    #####################################################################################
    # CALCULATIONS 
    ####################################################################################

    
    def calculate_tmin_pressure(self, temp_f=None, joint_type='Seamless') -> float:
        """
        Calculate minimum wall thickness for pressure design
        Based on ASME B31.1 Para. 304.1.2a Eq. 3a
        """
        D = self.get_OD()
        if D is None:
            raise ValueError(f"Invalid NPS {self.nps} for schedule {self.schedule}")
        
        S = self.S_allow['A-106 GR B']
        E = self.E_[joint_type]
        
       
        temp_str = str(temp_f)  # Get WSRF based on temperature
        W = self.WSRF.get(temp_str, 1.0)  # Default to 1.0 if temp not found, most process piping operate at temperatures below 950F
        
        Y = self.get_Y_coefficient()
        if Y is None:
            raise ValueError(f"No Y coefficient available for NPS {self.nps}")
        
        # ASME B31.1 Eq. 3a: t = (P*D)/(2*(S*E*W + P*Y))
        tmin_pressure = (self.pressure * D) / (2 * (S * E * W + self.pressure * Y))
        
        return tmin_pressure
    
    def tmin_structural(self) -> float:
        """API 574 Table D.2"""
        nps_key = float(self.nps)
        min_structural = self.API574_CS_400F[nps_key][self.pressure_class] #Only have 500F CS 
        return min_structural
    
    def life_span(self, excess, corrosion_rate) -> float:
        return np.floor(excess*corrosion_rate)


    # Old functions commented out for clarity and reference


    # def percent_RL(self, actual_thickness):
    #     """
    #     Calculate percentage of retirement limit (Table 5) remaining
    #     RL = actual thickness / retirement limit from Table 5
    #     """
    #     RL = self.table5_1_RL.get(self.nps)
    #     if RL is None:
    #         raise ValueError(f"No retirement limit available for NPS {self.nps}")
    #     percent_remaining = (actual_thickness / RL) * 100
    #     return percent_remaining

    # def check_RL_status(self, actual_thickness):
    #     """
    #     Check if pipe meets retirement limit requirements
    #     Returns status and percentage remaining
    #     """
    #     RL = self.table5_1_RL.get(self.nps)
    #     if RL is None:
    #         return {"status": "No RL data", "percent_remaining": None}
    #     percent_remaining = (actual_thickness / RL) * 100
    #     if actual_thickness >= RL:
    #         status = "Above RL"
    #     else:
    #         status = "Below RL - Consider Retirement"
    #     return {
    #         "status": status,
    #         "retirement_limit": RL,
    #         "actual_thickness": actual_thickness,
    #         "percent_remaining": percent_remaining
    #     }

    # def compare_thickness(self, actual_thickness, temp_f=1000, joint_type='Seamless'):
    #     """
    #     Comprehensive thickness analysis comparing actual vs calculated t-min and RL
    #     Returns comparison metrics for both pressure design and retirement limit
    #     """
    #     # Calculate pressure design requirements
    #     tmin = self.calculate_tmin_pressure(temp_f, joint_type)
    #     tmin_excess = actual_thickness - tmin
    #     tmin_percent_excess = (tmin_excess / actual_thickness) * 100
    #     # Check retirement limit
    #     rl_status = self.check_RL_status(actual_thickness)
    #     return {
    #         'actual_thickness': actual_thickness,
    #         'calculated_tmin': tmin,
    #         'tmin_excess': tmin_excess,
    #         'tmin_percent_excess': tmin_percent_excess,
    #         'rl_status': rl_status['status'],
    #         'retirement_limit': rl_status['retirement_limit'],
    #         'rl_percent_remaining': rl_status['percent_remaining'],
    #         'pressure_design_adequate': tmin_excess > 0,
    #         'rl_adequate': actual_thickness >= rl_status['retirement_limit'] if rl_status['retirement_limit'] else None
    #     }

    #####################################################################################
    # ANALYSIS
    ####################################################################################

    def analyze_pipe_thickness(self, actual_thickness, temp_f=1000, joint_type='Seamless'):
        """
        Analyze and compare all relevant thicknesses: pressure, structural, Table 5, and proposed retirement.
        Returns a dict with all relevant results and limiting factor.
        """
        
        tmin_pressure = self.calculate_tmin_pressure(temp_f, joint_type)
        tmin_structural = self.tmin_structural()

        
        # Use the provided default_retirement_limit if available
        default_retirement_limit = self.default_retirement_limit
        
        limits = {
            "pressure": tmin_pressure,
            "structural": tmin_structural,
            "table5": default_retirement_limit,
        }

        # limiting_type = min(limits, key=lambda k: limits[k] if limits[k] is not None else float('inf'))
        # limiting_thickness = limits[limiting_type]


        # Determines force contribution dictates the mechanical integrity and longevity of the pipe
        # The limiting thickness is the LARGER of pressure or structural tmin (i.e., the most conservative, requiring replacement at the highest threshold)
        if limits["pressure"] > limits["structural"]:
            limiting_thickness = limits["pressure"]
            limiting_type = "pressure"
        else:
            limiting_thickness = limits["structural"]
            limiting_type = "structural"

        print(f"Limiting thickness type: {limiting_type} at {limiting_thickness}")

        # How much below the defaulted Retirement Limit
        if default_retirement_limit is not None:
            if default_retirement_limit - actual_thickness >= 0:
                below_defaultRL = default_retirement_limit - actual_thickness
            else:
                print(f"Actual Thickness is greater than default retirement limit by {actual_thickness - default_retirement_limit}")
                below_defaultRL = None
        else:
            below_defaultRL = None
        
        #How much above the API574 Retirement Limit Code
        api574_value = self.which_API_table()
        if api574_value is not None:
            if api574_value < actual_thickness:
                corosion_allowance = actual_thickness - api574_value
            else:
                print(f"Actual Thickness is {api574_value - actual_thickness} inches below corresponding API 574 Structural Retirement Limit for {self.metallurgy}, Retire Immediately - Fit For Service assessment is needed")
                corosion_allowance = None
        else:
            corosion_allowance = None
        
        
        return {
            "tmin_pressure": tmin_pressure,
            "tmin_structural": tmin_structural,
            "default_retirement_limit": default_retirement_limit,
            "below_defaultRL": below_defaultRL,
            "api574_RL": self.which_API_table(), #Same as new, proposed retirement limit.
            "above_api574RL": corosion_allowance,
            "life_span": self.life_span(corosion_allowance, self.corrosion_rate) if corosion_allowance is not None and self.corrosion_rate is not None else None,
            #"proposed_retirement_limit": proposed_retirement_limit,
            "limiting_thickness": limiting_thickness,
            "limiting_type": limiting_type,
            #"status": status
        }

    def generate_full_report(self, actual_thickness: float, temp_f=1000, joint_type='Seamless') -> Dict[str, str]:
        """
        Generate a complete analysis with text report and visualizations
        
        Args:
            actual_thickness: The actual measured thickness
            temp_f: Temperature in Fahrenheit
            joint_type: Joint type for calculations
            
        Returns:
            Dict containing paths to generated files
        """
        from .report_generator import ReportGenerator
        from .visualization import ThicknessVisualizer
        
        # Perform analysis
        analysis_results = self.analyze_pipe_thickness(actual_thickness, temp_f, joint_type)
        
        # Generate reports
        report_gen = ReportGenerator()
        full_report_path = report_gen.generate_report(self, analysis_results, actual_thickness)
        summary_report_path = report_gen.generate_summary_report(self, analysis_results, actual_thickness)
        
        # Generate visualizations
        visualizer = ThicknessVisualizer()
        number_line_path = visualizer.create_thickness_number_line(analysis_results, actual_thickness)
        comparison_chart_path = visualizer.create_comparison_chart(analysis_results, actual_thickness)
        
        return {
            "full_report": full_report_path,
            "summary_report": summary_report_path,
            "number_line_plot": number_line_path,
            "comparison_chart": comparison_chart_path,
            "analysis_results": analysis_results
        }


# TODO

#   - Make Visualizer more readable and add visual tool and report explainations in README
#   - Add cli.py and __init__
#   - Add Setup.py, requirements.txt, makefile, ect.
#   - Fix allowable stress calculator
#   - Explain how to import properietary JSON files of piping maintenance defaults
#   - Add other metallurgy and temps to structural tmin py dictionaries
#   - Add other metallurgy yield strengths to py dictionaries under S_