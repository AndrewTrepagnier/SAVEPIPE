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

    trueID_10 = {
            '3/4' : 0.742,
            '1':  0.957,
            '1-1/4': 1.278,
            '1-1/2': 1.500,
            '2': 1.939,
            '2-1/2': 2.323,
            '3': 3.068,
            '3-1/2': 3.548,
            '4': 4.026
        }

    trueID_40 = {
        '3/8': 0.493,
        '1/2': 0.622,
        '3/4': 0.824,
        '1': 1.049,
        '1-1/4': 1.380,
        '1-1/2': 1.610,
        '2': 2.067,
        '2-1/2': 2.469,
        '3': 3.068,
        '3-1/2': 3.548,
        '4': 4.026,
        '5': 5.047,
        '6': 6.065,
        '8': 7.981,
        '10': 10.020,
        '12': 11.938,
        '14': 13.124,
        '16': 15.000,
        '18': 17.000,
        '20': 19.000,
        '24': 23.000
    }
    
    trueID_80 = {
        '3/8': 0.423,
        '1/2': 0.546,
        '3/4': 0.742,
        '1': 0.957,
        '1-1/4': 1.278,
        '1-1/2': 1.500,
        '2': 1.939,
        '2-1/2': 2.323,
        '3': 2.900,
        '3-1/2': 3.364,
        '4': 3.826,
        '5': 4.813,
        '6': 5.761,
        '8': 7.625,
        '10': 9.564,
        '12': 11.376,
        '14': 12.500,
        '16': 14.312,
        '18': 16.312,
        '20': 18.312,
        '24': 22.312
    }
    
    trueID_120 = {
        '1/2': 0.466,
        '3/4': 0.614,
        '1': 0.815,
        '1-1/4': 1.160,
        '1-1/2': 1.338,
        '2': 1.689,
        '2-1/2': 2.125,
        '3': 2.624,
        '3-1/2': 3.152,
        '4': 3.438,
        '5': 4.313,
        '6': 5.189,
        '8': 6.875,
        '10': 8.500,
        '12': 10.126,
        '14': 11.000,
        '16': 12.500,
        '18': 14.312,
        '20': 16.000,
        '24': 19.250
    }

    trueID_160 = {
        '1/2': 0.252,
        '3/4': 0.434,
        '1': 0.599,
        '1-1/4': 0.896,
        '1-1/2': 1.074,
        '2': 1.503,
        '2-1/2': 1.771,
        '3': 2.300,
        '3-1/2': 2.728,
        '4': 3.152,
        '5': 3.438,
        '6': 4.313,
        '8': 5.761,
        '10': 7.125,
        '12': 8.500,
        '14': 9.750,
        '16': 11.000,
        '18': 12.250,
        '20': 13.500,
        '24': 16.000
    }


    S_allow = {
        "A-106 GR B": 35000*(2/3) #Assuming pipe is A-106 GR B, Yield stress is 35000, take 2/3 fraction of it for allowable
    }
    # def t_D_ratio(self):
    #     if 

    def calculate_tmin(self):
        if self.schedule == "10":

            tmin = (self.pressure*self.trueID_10[self.nps]) / (2*(self.S_allow['A-106 GR B']*E*W + self.pressure*Y))

        elif self.schedule == '40':

            tmin = self.pressure*self.

        elif self.schedule == '80':

        elif self.schedule == '120':

        elif self.schedule == '160':

        return 