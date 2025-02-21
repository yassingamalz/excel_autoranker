# src/core/statistics_manager.py
from openpyxl import Workbook
import pandas as pd
from typing import List, Dict
import os
from .statistics.cronbach_alpha import CronbachAlphaCalculator
from .formatters.cronbach_formatter import CronbachFormatter

class StatisticsManager:
    def __init__(self, data: pd.DataFrame, questions: List[str], dimensions: Dict[str, List[str]]):
        self.data = data
        self.questions = questions
        self.dimensions = dimensions
        self.cronbach = CronbachAlphaCalculator()

    def analyze_and_export(self, output_dir: str = '/app/data/output') -> str:
        """
        Run statistical analysis and export to Excel
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create workbook
        wb = Workbook()
        
        # Calculate and format overall Cronbach's Alpha
        total_alpha_results = self.cronbach.calculate(self.data, self.questions)
        CronbachFormatter.format_results(wb, total_alpha_results)
        
        # Calculate and format dimensional Cronbach's Alpha
        for dim_num, dim_questions in self.dimensions.items():
            dim_alpha_results = self.cronbach.calculate(self.data, dim_questions)
            if dim_alpha_results['status'] == 'success':
                dim_sheet = wb.create_sheet(title=f"Dimension {dim_num}")
                CronbachFormatter.format_results_to_sheet(dim_sheet, dim_alpha_results)
        
        # Save workbook
        output_file = os.path.join(output_dir, 'statistical_analysis.xlsx')
        wb.save(output_file)
        
        return output_file