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

    def calculate_per_question_alpha(self) -> Dict:
        """Calculate Cronbach's Alpha excluding each question one at a time"""
        per_question_results = {}
        
        self.logger.info("Calculating per-question Cronbach's Alpha")
        
        # Calculate baseline alpha with all questions
        baseline_alpha = self.cronbach.calculate(self.data, self.questions)['alpha']
        
        for question in self.questions:
            # Create list of questions excluding current one
            remaining_questions = [q for q in self.questions if q != question]
            
            # Calculate alpha without this question
            alpha_without = self.cronbach.calculate(self.data, remaining_questions)['alpha']
            
            # Store results
            per_question_results[question] = {
                'alpha_if_deleted': alpha_without,
                'alpha_change': alpha_without - baseline_alpha
            }
            
            self.logger.debug(f"Question {question}: Alpha if deleted = {alpha_without:.4f}, Change = {alpha_without - baseline_alpha:.4f}")
        
        return per_question_results

    def analyze_and_export(self, output_dir: str = '/app/data/output') -> str:
        """Run statistical analysis and export to Excel"""
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

            # Add per-question analysis sheet
            per_question_sheet = wb.create_sheet(title="Question Analysis")
            self.format_per_question_results(per_question_sheet)
            
            # Save workbook
            output_file = os.path.join(output_dir, 'statistical_analysis.xlsx')
            wb.save(output_file)
            self.logger.info(f"Analysis exported to {output_file}")
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error in analyze_and_export: {str(e)}")
            raise

    def format_per_question_results(self, ws):
        """Format per-question analysis results in worksheet"""
        # Headers
        headers = [
            "Question / السؤال",
            "Alpha if Deleted / معامل ألفا عند الحذف",
            "Change in Alpha / التغير في معامل ألفا",
            "Impact / التأثير"
        ]
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            CronbachFormatter._apply_header_style(cell)
        
        # Calculate per-question results
        results = self.calculate_per_question_alpha()
        
        # Add data rows
        for row, (question, data) in enumerate(results.items(), 2):
            ws.cell(row=row, column=1, value=question)
            ws.cell(row=row, column=2, value=round(data['alpha_if_deleted'], 6))
            change = data['alpha_change']
            ws.cell(row=row, column=3, value=round(change, 6))
            
            # Add impact interpretation
            impact = ("Improves reliability / يحسن الثبات" if change > 0 else 
                     "Reduces reliability / يقلل الثبات" if change < 0 else 
                     "No impact / لا تأثير")
            ws.cell(row=row, column=4, value=impact)
            
            # Apply styling to all cells in row
            for col in range(1, 5):
                CronbachFormatter._apply_data_style(ws.cell(row=row, column=col))
        
        # Adjust column widths
        CronbachFormatter._adjust_column_widths(ws)