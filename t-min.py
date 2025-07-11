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
    
    # Valid pipe types for reference
    VALID_PIPE_TYPES = ["straight", "bend-90", "bend-45", "tee", "elbow"]
    
    # Valid schedules for reference
    VALID_SCHEDULES = ["10", "40", "80", "120", "160"]

    #########################

    # with open('newjsonfile', 'r') as file:
    #     data = json.load(file)

    # with open('newjsonfile', 'r') as file:
    #     data = json.load(file)

    ###########################

    trueOD_10 = {
            '3/4' : 1.050,
            '1':  1.315,
            '1-1/4': 1.660,
            '1-1/2': 1.900,
            '2': 2.375,
            '2-1/2': 2.875,
            '3': 3.500,
            '3-1/2': 4.000,
            '4': 4.500
        }

    trueOD_40 = {
        '3/8': 0.675,
        '1/2': 0.840,
        '3/4': 1.050,
        '1': 1.315,
        '1-1/4': 1.660,
        '1-1/2': 1.900,
        '2': 2.375,
        '2-1/2': 2.875,
        '3': 3.500,
        '3-1/2': 4.000,
        '4': 4.500,
        '5': 5.563,
        '6': 6.625,
        '8': 8.625,
        '10': 10.750,
        '12': 12.750,
        '14': 14.000,
        '16': 16.000,
        '18': 18.000,
        '20': 20.000,
        '24': 24.000
    }
    
    trueOD_80 = {
        '3/8': 0.675,
        '1/2': 0.840,
        '3/4': 1.050,
        '1': 1.315,
        '1-1/4': 1.660,
        '1-1/2': 1.900,
        '2': 2.375,
        '2-1/2': 2.875,
        '3': 3.500,
        '3-1/2': 4.000,
        '4': 4.500,
        '5': 5.563,
        '6': 6.625,
        '8': 8.625,
        '10': 10.750,
        '12': 12.750,
        '14': 14.000,
        '16': 16.000,
        '18': 18.000,
        '20': 20.000,
        '24': 24.000
    }
    
    trueOD_120 = {
        '1/2': 0.840,
        '3/4': 1.050,
        '1': 1.315,
        '1-1/4': 1.660,
        '1-1/2': 1.900,
        '2': 2.375,
        '2-1/2': 2.875,
        '3': 3.500,
        '3-1/2': 4.000,
        '4': 4.500,
        '5': 5.563,
        '6': 6.625,
        '8': 8.625,
        '10': 10.750,
        '12': 12.750,
        '14': 14.000,
        '16': 16.000,
        '18': 18.000,
        '20': 20.000,
        '24': 24.000
    }

    trueOD_160 = {
        '1/2': 0.840,
        '3/4': 1.050,
        '1': 1.315,
        '1-1/4': 1.660,
        '1-1/2': 1.900,
        '2': 2.375,
        '2-1/2': 2.875,
        '3': 3.500,
        '3-1/2': 4.000,
        '4': 4.500,
        '5': 5.563,
        '6': 6.625,
        '8': 8.625,
        '10': 10.750,
        '12': 12.750,
        '14': 14.000,
        '16': 16.000,
        '18': 18.000,
        '20': 20.000,
        '24': 24.000
    }

    WSRF = { # weld strength reduction factor, Provide Farenheit and returns weld factor, W
        '1250': 0.73,
        '1300' : 0.68,
        '1350': 0.63,
        '1400': 0.59,
        '1450': 0.55,
        '1500': 0.5
    }

    S_allow = {
        'A-106 GR B': 35000*(2/3) #Assuming pipe is A-106 GR B, Yield stress is 35000, take 2/3 fraction of it for allowable
    }

    E_ = {
        'Seamless': 1.00,
        'Furnace Butt Welded': 0.60,
        'Electric Resistance Welded': 0.85
    }

    ###########################################################
    # See table of y coefficients in Table 104.1.2-1 ASME B31.1

    ferritic_steels_y = {
        900: 0.4,
        950: 0.5,
        1000: 0.7,
        1050: 0.7,
        1100: 0.7,
        1150: 0.7,
        1200: 0.7,
        1250: 0.7
    }

    austenitic_steels_y = {
        900: 0.4,
        950: 0.4,
        1000: 0.4,
        1050: 0.4,
        1100: 0.5,
        1150: 0.7,
        1200: 0.7,
        1250: 0.7
    }

    nickel_alloy_N06690_y = {
        900: 0.4,
        950: 0.4,
        1000: 0.4,
        1050: 0.4,
        1100: 0.5,
        1150: 0.7,
        1200: 0.7,
        1250: None  # Not applicable ("...")
    }

    nickel_alloys_N06617_N08800_N08810_N08825_y = {
        900: 0.4,
        950: 0.4,
        1000: 0.4,
        1050: 0.4,
        1100: 0.4,
        1150: 0.4,
        1200: 0.5,
        1250: 0.7
    }

    cast_iron_y = {
        900: 0.0,
        950: None,
        1000: None,
        1050: None,
        1100: None,
        1150: None,
        1200: None,
        1250: None
    }

    other_metals_y = {
        900: 0.4,
        950: 0.4,
        1000: 0.4,
        1050: 0.4,
        1100: 0.4,
        1150: 0.4,
        1200: 0.4,
        1250: 0.4
    }

    ##########################################################
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
        tmin = (self.pressure * D) / (2 * (S * E * W + self.pressure * Y))
        
        return tmin

    def calculate_tmin_structural(self):
        """
        Calculate minimum wall thickness for structural requirements
        This would include bending, torsion, etc.
        """
        # Placeholder for structural calculations
        # Would include bending stress, torsion, etc.
        return 0.0

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

    def analyze_pipe_thickness(self, actual_thickness, temp_f=1000, joint_type='Seamless', proposed_retirement_limit=None):
        """
        Analyze and compare all relevant thicknesses: pressure, structural, Table 5, and proposed retirement.
        Returns a dict with all relevant results and limiting factor.
        """
        # 1. Calculate pressure tmin
        tmin_pressure = self.calculate_tmin_pressure(temp_f, joint_type)
        # 2. Calculate structural tmin (placeholder)
        tmin_structural = self.calculate_tmin_structural()
        # 3. Get Table 5 retirement limit from JSON
        import json
        with open('table5.JSON', 'r') as f:
            table5 = json.load(f)
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
