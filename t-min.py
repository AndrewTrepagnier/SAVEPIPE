import numpy as np
from dataclasses import dataclass
from typing import Literal

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

    # See table of y coefficients in Table 104.1.2-1 ASME B31.1
    table5_1_RL = {
        '3/4': 0.083,
        '1': 0.083,
        '1-1/4': 0.083,
        '1-1/2': 0.083,
        '2': 0.083,
        '2-1/2': None,
        '3': 0.134,
        '3-1/2': 0.134,
        '4': 0.134,
        '5': 0.134,
        '6': 0.134,
        '8': 0.134,
        '10': 0.134,
        '12': 0.134,
        '14': 0.134,
        '16': 0.134,
        '18': 0.134,
        '20': 0.148,
        '22': 0.148,
        '24': 0.165
    }

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
        return self.table5_1_RL.get(self.nps)

    def calculate_tmin_pressure(self, temp_f=1000, joint_type='Seamless'):
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
        W = self.WSRF.get(temp_str, 1.0)  # Default to 1.0 if temp not found
        
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

    def percent_RL(self, actual_thickness):
        """
        Calculate percentage of retirement limit remaining
        RL = actual thickness - minimum required thickness
        """
        tmin = self.calculate_tmin_pressure()
        RL = actual_thickness - tmin
        percent_remaining = (RL / actual_thickness) * 100
        return percent_remaining

    def compare_thickness(self, actual_thickness):
        """
        Compare actual vs calculated minimum thickness
        Returns comparison metrics
        """
        tmin = self.calculate_tmin_pressure()
        excess = actual_thickness - tmin
        percent_excess = (excess / actual_thickness) * 100
        
        return {
            'actual_thickness': actual_thickness,
            'calculated_tmin': tmin,
            'excess_thickness': excess,
            'percent_excess': percent_excess,
            'percent_RL_remaining': self.percent_RL(actual_thickness)
        }