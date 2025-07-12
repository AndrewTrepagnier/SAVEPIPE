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
        Create a number line visualization showing all thickness values
        
        Args:
            analysis_results: Results from analyze_pipe_thickness method
            actual_thickness: The actual measured thickness
            filename: Optional filename to save the plot (without extension)
            
        Returns:
            str: Path to saved image file
        """
        
        # Extract values from analysis results
        tmin_pressure = analysis_results.get('tmin_pressure', 0)
        tmin_structural = analysis_results.get('tmin_structural', 0)
        default_retirement_limit = analysis_results.get('default_retirement_limit', 0)
        api574_RL = analysis_results.get('api574_RL', 0)
        limiting_thickness = analysis_results.get('limiting_thickness', 0)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create number line
        all_values = [actual_thickness, tmin_pressure, tmin_structural, 
                     default_retirement_limit, api574_RL, limiting_thickness]
        min_val = min([v for v in all_values if v is not None and v > 0]) * 0.8
        max_val = max([v for v in all_values if v is not None]) * 1.2
        
        # Plot number line
        ax.plot([min_val, max_val], [0, 0], 'k-', linewidth=2, alpha=0.3)
        
        # Plot each thickness value
        y_positions = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
        labels = []
        
        # Actual thickness
        if actual_thickness is not None:
            ax.scatter(actual_thickness, y_positions[0], color=self.colors['actual'], 
                      s=100, zorder=5, label='Actual Thickness')
            ax.axvline(actual_thickness, color=self.colors['actual'], alpha=0.3, linestyle='--')
            labels.append(f'Actual: {actual_thickness:.4f}"')
        
        # Pressure design minimum
        if tmin_pressure is not None:
            ax.scatter(tmin_pressure, y_positions[1], color=self.colors['pressure'], 
                      s=100, zorder=5, label='Pressure Design Min')
            ax.axvline(tmin_pressure, color=self.colors['pressure'], alpha=0.3, linestyle='--')
            labels.append(f'Pressure Min: {tmin_pressure:.4f}"')
        
        # Structural minimum
        if tmin_structural is not None:
            ax.scatter(tmin_structural, y_positions[2], color=self.colors['structural'], 
                      s=100, zorder=5, label='Structural Min')
            ax.axvline(tmin_structural, color=self.colors['structural'], alpha=0.3, linestyle='--')
            labels.append(f'Structural Min: {tmin_structural:.4f}"')
        
        # Table 5 retirement limit
        if default_retirement_limit is not None:
            ax.scatter(default_retirement_limit, y_positions[3], color=self.colors['table5'], 
                      s=100, zorder=5, label='Table 5 RL')
            ax.axvline(default_retirement_limit, color=self.colors['table5'], alpha=0.3, linestyle='--')
            labels.append(f'Table 5 RL: {default_retirement_limit:.4f}"')
        
        # API 574 retirement limit
        if api574_RL is not None:
            ax.scatter(api574_RL, y_positions[4], color=self.colors['api574'], 
                      s=100, zorder=5, label='API 574 RL')
            ax.axvline(api574_RL, color=self.colors['api574'], alpha=0.3, linestyle='--')
            labels.append(f'API 574 RL: {api574_RL:.4f}"')
        
        # Limiting thickness
        if limiting_thickness is not None:
            ax.scatter(limiting_thickness, y_positions[5], color=self.colors['limiting'], 
                      s=150, zorder=6, label='Limiting Thickness', marker='*')
            ax.axvline(limiting_thickness, color=self.colors['limiting'], alpha=0.5, linewidth=2)
            labels.append(f'Limiting: {limiting_thickness:.4f}"')
        
        # Customize the plot
        ax.set_xlim(min_val, max_val)
        ax.set_ylim(-0.5, 1.5)
        ax.set_xlabel('Thickness (inches)', fontsize=12, fontweight='bold')
        ax.set_title('Pipe Thickness Analysis - Number Line View', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', bbox_to_anchor=(1, 1))
        
        # Add text annotations
        for i, label in enumerate(labels):
            if i < len(y_positions):
                ax.text(max_val * 1.05, y_positions[i], label, fontsize=10, 
                       verticalalignment='center')
        
        # Add status information
        limiting_type = analysis_results.get('limiting_type', 'Unknown')
        status_text = f"Limiting Factor: {limiting_type}"
        ax.text(0.02, 0.98, status_text, transform=ax.transAxes, fontsize=12,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Save the plot
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
            'Table 5 RL': analysis_results.get('default_retirement_limit', 0),
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