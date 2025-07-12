from .asmetables.od_tables import trueOD_40, trueOD_80, ...
from .asmetables.weld_factors import WSRF
from .asmetables.y_factors import ferritic_steels_y, ...
from .asmetables.yield_stress import S_, E_
from .asmetables.structural_tmin import API574_CS_400F

import numpy as np
from dataclasses import dataclass
from typing import Literal
import json

@dataclass
class SAVEPIPE:

    #run: str  
    schedule: str  # Pipe schedule (10, 40, 80, 120, 160)
    nps: str  # Nominal pipe size (e.g., '2', '3/4', '1-1/2')
    pressure: float  # Design pressure (psi)
    pipe_config: Literal["straight", "bend-90", "bend-45", "tee", "elbow"] = "straight"  # Pipe configuration
    pressure_class: Literal[150, 300, 600, 900, 1500, 2500]


    # Valid pipe types for reference
    VALID_PIPE_TYPES = ["straight", "bend-90", "bend-45", "tee", "elbow"]
    
    # Valid schedules for reference
    VALID_SCHEDULES = ["10", "40", "80", "120", "160"]

    #########################
    # Add propreitary JSON file or CSV of retirement limit structural thicknesses below to be considered into the analysis, if not, comment out

    def load_table(self):
        with open('table5.JSON', 'r') as file:
            return json.load(file)
        
    


    def allowable(self, Syield):
        return Syield*(2/3)

    def get_OD(self):
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

    def get_Y_coefficient(self):
        """Get Y coefficient from ASME B31.1 Table 104.1.2-1"""
        return self.ferritic_steels_y[900] # For most process CS pipes, the y coefficient for 900°F (482°C) and below is used, which is y = 0.4 for ferritic steels (the most common type of CS pipe)
    
    #####################################################################################
    # CALCULATIONS 
    ####################################################################################

    

    def calculate_tmin_pressure(self, temp_f=None, joint_type='Seamless'):
        """
        Calculate minimum wall thickness for pressure design
        Based on ASME B31.1 Para. 304.1.2a Eq. 3a
        """
        D = self.get_OD()
        if D is None:
            raise ValueError(f"Invalid NPS {self.nps} for schedule {self.schedule}")
        

        
        S = self.S_allow['A-106 GR B']
        E = self.E_[joint_type]


        
        # Get WSRF based on temperature
        temp_str = str(temp_f)
        W = self.WSRF.get(temp_str, 1.0)  # Default to 1.0 if temp not found, most process piping operate at temperatures below 950F
        


        Y = self.get_Y_coefficient()
        if Y is None:
            raise ValueError(f"No Y coefficient available for NPS {self.nps}")
        


        # ASME B31.1 Eq. 3a: t = (P*D)/(2*(S*E*W + P*Y))
        tmin_pressure = (self.pressure * D) / (2 * (S * E * W + self.pressure * Y))
        
        return tmin_pressure
    
    def tmin_structural(self):
        """API 574 Table D.2"""
        min_structural = self.API574_CS_400F[self.nps][self.pressure_class] #Only have 500F CS 
        return min_structural
    


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

    def analyze_pipe_thickness(self, actual_thickness, temp_f=1000, joint_type='Seamless', proposed_retirement_limit=None):
        """
        Analyze and compare all relevant thicknesses: pressure, structural, Table 5, and proposed retirement.
        Returns a dict with all relevant results and limiting factor.
        """
        
        tmin_pressure = self.calculate_tmin_pressure(temp_f, joint_type)
        
        tmin_structural = self.tmin_structural()
        # 3. Get Table 5 retirement limit from JSON
        



        table5_retirement_limit = table5.get(self.nps)
        # 4. Proposed retirement limit (user input or logic)
        if proposed_retirement_limit is None:
            proposed_retirement_limit = table5_retirement_limit  # fallback
        # 5. Find limiting thickness
        limits = {
            "pressure": tmin_pressure,
            "structural": tmin_structural,
            "table5": table5_retirement_limit,
            "proposed": proposed_retirement_limit
        }
        limiting_type = min(limits, key=lambda k: limits[k] if limits[k] is not None else float('inf'))
        limiting_thickness = limits[limiting_type]
        # 6. How much below Table 5?
        amount_below_table5 = (table5_retirement_limit - actual_thickness) if (table5_retirement_limit and actual_thickness < table5_retirement_limit) else 0
        # 7. Status
        if actual_thickness < table5_retirement_limit:
            status = "Below Table 5"
        else:
            status = "OK"
        return {
            "tmin_pressure": tmin_pressure,
            "tmin_structural": tmin_structural,
            "table5_retirement_limit": table5_retirement_limit,
            "proposed_retirement_limit": proposed_retirement_limit,
            "limiting_thickness": limiting_thickness,
            "limiting_type": limiting_type,
            "amount_below_table5": amount_below_table5,
            "status": status
        }


#USAGE EXAMPLE

pipe = SAVEPIPE("40", "2", 500.0, "straight")

# Comprehensive analysis
results = pipe.analyze_pipe_thickness(actual_thickness=0.060)

# print(f"Pressure Design: {results['pressure_design_adequate']}")
# print(f"RL Status: {results['rl_status']}")
# print(f"RL % Remaining: {results['rl_percent_remaining']:.1f}%")






# TODO: Implement logic to propose new retirement limits
# The new retirement limit should be based on:
#   - Corrosion rates (as determined by inspection and process teams)
#   - Remaining service life requirements
#   - Regulatory or company standards
# This may require:
#   - Accepting corrosion rate as an input (e.g., mils per year)
#   - Calculating remaining life based on current thickness, corrosion rate, and required future service duration
#   - Setting the new retirement limit to ensure safe operation until next planned inspection or end of service life
#   - Add other metallurgy and temps to structural tmin py dictionaries
#   - Add other metallurgy yield strengths to py dictionaries under S_