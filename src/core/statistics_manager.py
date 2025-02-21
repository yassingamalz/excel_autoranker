# src/core/statistics_manager.py
from openpyxl import Workbook
import pandas as pd
import logging
from typing import List, Dict
import os
from .statistics.cronbach_alpha import CronbachAlphaCalculator
from .formatters.cronbach_formatter import CronbachFormatter

class StatisticsManager:
    def __init__(self, data: pd.DataFrame, questions: List[str], dimensions: Dict[str, List[str]]):
        self.logger = logging.getLogger('ExcelAutoRanker')
        self.data = data
        self.questions = questions
        self.dimensions = dimensions
        self.cronbach = CronbachAlphaCalculator()
        
        self.logger.info("\n" + "="*80)
        self.logger.info("STATISTICS CALCULATION SETUP")
        self.logger.info(f"Total questions: {len(questions)}")
        self.logger.info(f"Total dimensions: {len(dimensions)}")
        self.logger.info("-"*80)
        self.logger.info("DIMENSIONS BREAKDOWN:")
        for dim_num, dim_cols in dimensions.items():
            self.logger.info(f"Dimension {dim_num} ({len(dim_cols)} questions):")
            self.logger.info(f"Questions: {','.join(dim_cols)}")
            self.logger.info("-"*40)

    def analyze_and_export(self, output_dir: str = '/app/data/output') -> str:
        """
        Run statistical analysis and export to Excel
        """
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Create workbook
            wb = Workbook()
            
            # Calculate and format overall Cronbach's Alpha
            self.logger.info("Calculating total Cronbach's Alpha")
            total_alpha_results = self.cronbach.calculate(self.data, self.questions)
            self.logger.info(f"Total Cronbach's Alpha: {total_alpha_results.get('alpha', 'N/A')}")
            CronbachFormatter.format_results(wb, total_alpha_results)
            
            # Calculate and format dimensional Cronbach's Alpha
            self.logger.info("Calculating dimensional Cronbach's Alpha")
            for dim_num, dim_questions in self.dimensions.items():
                self.logger.debug(f"Processing dimension {dim_num} with {len(dim_questions)} questions")
                self.logger.debug(f"Dimension {dim_num} questions: {dim_questions}")
                
                dim_alpha_results = self.cronbach.calculate(self.data, dim_questions)
                self.logger.info(f"Dimension {dim_num} Cronbach's Alpha: {dim_alpha_results.get('alpha', 'N/A')}")
                
                if dim_alpha_results['status'] == 'success':
                    dim_sheet = wb.create_sheet(title=f"Dimension {dim_num}")
                    CronbachFormatter.format_results_to_sheet(dim_sheet, dim_alpha_results)
                else:
                    self.logger.error(f"Failed to calculate Cronbach's Alpha for dimension {dim_num}")
            
            # Save workbook
            output_file = os.path.join(output_dir, 'statistical_analysis.xlsx')
            wb.save(output_file)
            self.logger.info(f"Analysis exported to {output_file}")
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error in analyze_and_export: {str(e)}")
            raise