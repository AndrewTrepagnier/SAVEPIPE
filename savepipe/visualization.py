import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import os

class ThicknessVisualizer:
    """
    Creates visualizations for pipe thickness analysis including number line plots
    showing actual thickness, pressure design requirements, structural requirements, etc.
    """
    
    def __init__(self):
        self.colors = {
            'actual': 'blue',
            'pressure': 'red', 
            'structural': 'green',
            'table5': 'orange',
            'api574': 'purple',
            'limiting': 'black'
        }
        # Create Reports directory if it doesn't exist
        self.reports_dir = "Reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def _get_filename_with_date(self, base_name: str, filename: Optional[str] = None) -> str:
        """Generate filename with date prefix"""
        if filename is None:
            date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{date_str}_{base_name}"
        
        return os.path.join(self.reports_dir, filename)
    
    def create_thickness_number_line(self, analysis_results: Dict[str, Any], 
                                   actual_thickness: float, 
                                   filename: Optional[str] = None) -> str:
        """
        Create a number line visualization: x=0 is ID, x=OD is OD, and all thicknesses are measured from OD back toward ID.
        """
        # Extract values
        tmin_pressure = analysis_results.get('tmin_pressure', 0)
        api574_RL = analysis_results.get('api574_RL', 0)
        default_retirement_limit = analysis_results.get('default_retirement_limit', 0)
        # Get OD and ID from pipe instance if available
        pipe = analysis_results.get('pipe', None)
        if pipe is not None and hasattr(pipe, 'get_OD') and hasattr(pipe, 'get_ID'):
            OD = pipe.get_OD()
            ID = pipe.get_ID()
        else:
            # Fallback: use max value for OD, 0 for ID
            OD = max([actual_thickness, tmin_pressure, api574_RL]) * 2
            ID = 0
        # All thicknesses are measured from OD back toward ID
        x_actual = OD - actual_thickness
        x_api574 = OD - api574_RL
        x_pressure = OD - tmin_pressure
        x_table5 = OD - default_retirement_limit
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 3))
        # Shade fluid region (from ID to actual thickness)
        ax.axvspan(ID, x_actual, color='deepskyblue', alpha=0.3, label='Fluid')
        # Shade pipe wall region (from actual thickness to OD)
        ax.axvspan(x_actual, OD, color='lightgrey', alpha=0.5, label='Remaining Pipe Wall')
        # Draw OD as thick grey line
        ax.axvline(OD, color='grey', linewidth=10, alpha=0.7, label='OD')
        # Draw ID as y-axis (x=0)
        ax.axvline(ID, color='black', linewidth=2, linestyle='-', label='Nominal ID')
        # Draw actual thickness
        ax.axvline(x_actual, color=self.colors['actual'], linewidth=3, label='Actual Thk.')
        # Draw API 574 RL
        ax.axvline(x_api574, color=self.colors['api574'], linewidth=2, linestyle='--', label='API 574 RL')
        # Draw Retirement Limit
        ax.axvline(x_table5, color=self.colors['table5'], linewidth=2, linestyle='--', label='Retirement Limit')
        # Draw pressure min
        ax.axvline(x_pressure, color=self.colors['pressure'], linewidth=2, linestyle='--', label='Min. Pressure Thk.')
        # Customize
        ax.set_xlim(ID - 0.1 * (OD - ID), OD + 0.1 * (OD - ID))
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([0])
        ax.set_yticklabels([''])
        ax.set_xlabel('Profile of Pipe Wall', fontsize=12, fontweight='bold')
        # Remove the top title
        # ax.set_title('Pipe Wall Thickness Profile', fontsize=14, fontweight='bold')
        ax.grid(True, which='both', axis='x', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_linewidth(1.5)
        # Move legend outside plot to the right
        ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0., frameon=True)
        # Annotate: Move all labels to the top of the plot and rotate them to be parallel with the lines
        y_label = 0.45  # Top of the plot
        label_kwargs = dict(fontsize=10, ha='center', va='bottom', fontweight='bold', rotation=90)
        ax.text(OD, y_label, '      Outer Dia.', color='grey', **label_kwargs)
        ax.text(ID, y_label, '     Nominal Inner Dia.', color='black', **label_kwargs)
        ax.text(x_actual, y_label, '     Actual Inner Dia.', color=self.colors['actual'], **label_kwargs)
        ax.text(x_api574, y_label, '     API 574 Retirement Limit', color=self.colors['api574'], **label_kwargs)
        ax.text(x_table5, y_label, '     Retirement Limit', color=self.colors['table5'], **label_kwargs)
        ax.text(x_pressure, y_label, '      Min. Pressure Containing Thk.', color=self.colors['pressure'], **label_kwargs)
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        filepath = self._get_filename_with_date("thickness_analysis_number_line")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    
    def create_comparison_chart(self, analysis_results: Dict[str, Any], 
                              actual_thickness: float,
                              filename: Optional[str] = None) -> str:
        """
        Create a bar chart comparing different thickness values
        
        Args:
            analysis_results: Results from analyze_pipe_thickness method
            actual_thickness: The actual measured thickness
            filename: Optional filename to save the plot (without extension)
            
        Returns:
            str: Path to saved image file
        """
        
        # Extract values
        values = {
            'Actual': actual_thickness,
            'Pressure Min': analysis_results.get('tmin_pressure', 0),
            'Structural Min': analysis_results.get('tmin_structural', 0),
            'Retirement Limit': analysis_results.get('default_retirement_limit', 0),
            'API 574 RL': analysis_results.get('api574_RL', 0)
        }
        
        # Filter out None values
        values = {k: v for k, v in values.items() if v is not None}
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(values.keys())
        thickness_values = list(values.values())
        colors = [self.colors.get(cat.lower().replace(' ', ''), 'gray') for cat in categories]
        
        bars = ax.bar(categories, thickness_values, color=colors, alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, thickness_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                   f'{value:.4f}"', ha='center', va='bottom', fontweight='bold')
        
        # Highlight the limiting factor
        limiting_type = analysis_results.get('limiting_type', '')
        if limiting_type == 'pressure':
            limiting_label = 'Pressure Min'
        elif limiting_type == 'structural':
            limiting_label = 'Structural Min'
        else:
            limiting_label = None
            
        if limiting_label and limiting_label in categories:
            idx = categories.index(limiting_label)
            bars[idx].set_edgecolor('black')
            bars[idx].set_linewidth(3)
        
        ax.set_ylabel('Thickness (inches)', fontsize=12, fontweight='bold')
        ax.set_title('Pipe Thickness Comparison', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save the plot
        filepath = self._get_filename_with_date("thickness_comparison_chart")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath 