import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
import os

class ThicknessVisualizer:
    """
    Creates visualizations for pipe thickness analysis
    """
    
    def __init__(self):
        self.reports_dir = "Reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def _get_filename_with_date(self, base_name: str, filename: Optional[str] = None) -> str:
        """Generate filename with date prefix"""
        if filename is None:
            date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{date_str}_{base_name}"
        
        return os.path.join(self.reports_dir, filename)
    
    def create_thickness_number_line(self, analysis_results: Dict[str, Any], 
                                   actual_thickness: float, filename: Optional[str] = None) -> str:
        """
        Create a number line visualization showing all thickness values
        
        Args:
            analysis_results: Results from analyze_pipe_thickness method
            actual_thickness: The actual measured thickness
            filename: Optional filename to save the plot (without extension)
            
        Returns:
            str: Path to saved plot file
        """
        
        # Extract values
        tmin_pressure = analysis_results.get('tmin_pressure', 0)
        tmin_structural = analysis_results.get('tmin_structural', 0)
        api574_RL = analysis_results.get('api574_RL', 0)
        retirement_limit = analysis_results.get('default_retirement_limit', None)
        limiting_thickness = analysis_results.get('limiting_thickness', 0)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Define positions for vertical lines
        positions = []
        labels = []
        colors = []
        
        # Add actual thickness
        positions.append(actual_thickness)
        labels.append('Actual Thickness')
        colors.append('blue')
        
        # Add pressure design minimum
        positions.append(tmin_pressure)
        labels.append('Pressure Design t-min')
        colors.append('red')
        
        # Add structural minimum
        positions.append(tmin_structural)
        labels.append('Structural t-min')
        colors.append('orange')
        
        # Add API 574 retirement limit
        if api574_RL:
            positions.append(api574_RL)
            labels.append('API 574 RL')
            colors.append('purple')
        
        # Add retirement limit
        if retirement_limit:
            positions.append(retirement_limit)
            labels.append('Retirement Limit')
            colors.append('green')
        
        # Add limiting thickness
        positions.append(limiting_thickness)
        labels.append('Limiting Thickness')
        colors.append('darkred')
        
        # Create vertical lines
        for pos, label, color in zip(positions, labels, colors):
            ax.axvline(x=pos, color=color, linestyle='-', linewidth=2, label=label)
        
        # Set x-axis limits
        min_val = min(positions) * 0.8
        max_val = max(positions) * 1.2
        ax.set_xlim(min_val, max_val)
        
        # Customize plot
        ax.set_xlabel('Thickness (inches)', fontsize=12)
        ax.set_title('TMIN - Pipe Thickness Analysis', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Add text annotations
        for pos, label in zip(positions, labels):
            ax.text(pos, ax.get_ylim()[1] * 0.9, f'{pos:.4f}"', 
                   rotation=90, ha='center', va='top', fontsize=10)
        
        plt.tight_layout()
        
        # Save plot
        if filename is None:
            filename = f"thickness_analysis_number_line"
        
        filepath = self._get_filename_with_date(f"{filename}.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_comparison_chart(self, analysis_results: Dict[str, Any], 
                               actual_thickness: float, filename: Optional[str] = None) -> str:
        """
        Create a bar chart comparing different thickness values
        
        Args:
            analysis_results: Results from analyze_pipe_thickness method
            actual_thickness: The actual measured thickness
            filename: Optional filename to save the plot (without extension)
            
        Returns:
            str: Path to saved plot file
        """
        
        # Extract values
        tmin_pressure = analysis_results.get('tmin_pressure', 0)
        tmin_structural = analysis_results.get('tmin_structural', 0)
        api574_RL = analysis_results.get('api574_RL', 0)
        retirement_limit = analysis_results.get('default_retirement_limit', None)
        limiting_thickness = analysis_results.get('limiting_thickness', 0)
        
        # Prepare data for plotting
        categories = ['Actual', 'Pressure t-min', 'Structural t-min', 'Limiting']
        values = [actual_thickness, tmin_pressure, tmin_structural, limiting_thickness]
        colors = ['blue', 'red', 'orange', 'darkred']
        
        # Add API 574 RL if available
        if api574_RL:
            categories.append('API 574 RL')
            values.append(api574_RL)
            colors.append('purple')
        
        # Add retirement limit if available
        if retirement_limit:
            categories.append('Retirement Limit')
            values.append(retirement_limit)
            colors.append('green')
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bars
        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.4f}"', ha='center', va='bottom')
        
        # Customize plot
        ax.set_ylabel('Thickness (inches)', fontsize=12)
        ax.set_title('TMIN - Thickness Comparison Chart', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save plot
        if filename is None:
            filename = f"thickness_comparison_chart"
        
        filepath = self._get_filename_with_date(f"{filename}.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath 