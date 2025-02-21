# src/core/statistics/construct_validity.py
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os
from typing import Dict, List

class ConstructValidityCalculator:
    def __init__(self):
        self._setup_logger()
        
    def _setup_logger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        self.logger = logging.getLogger('ConstructValidity')
        self.logger.setLevel(logging.DEBUG)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/construct_validity_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)

    def calculate(self, data: pd.DataFrame, questions: List[str], dimensions: Dict[str, List[str]]) -> Dict:
        """
        Calculate Spearman's Construct Validity
        """
        self.logger.info(f"Starting Construct Validity calculation")
        self.logger.debug(f"Total questions: {len(questions)}")
        self.logger.debug(f"Number of dimensions: {len(dimensions)}")

        try:
            # Convert to numeric and handle missing values
            df = data[questions].apply(pd.to_numeric, errors='coerce')
            df_clean = df.dropna()
            
            # Calculate total scores and ranks for each participant
            total_scores = df_clean[questions].sum(axis=1)
            total_ranks = total_scores.rank(method='average')
            
            dimension_results = {}
            correlations = {}
            
            # Calculate dimension scores, ranks and correlations
            for dim_num, dim_questions in dimensions.items():
                self.logger.debug(f"Processing dimension {dim_num}")
                
                # Calculate dimension scores and ranks
                dim_scores = df_clean[dim_questions].sum(axis=1)
                dim_ranks = dim_scores.rank(method='average')
                
                # Calculate Spearman correlation with total ranks
                correlation = total_ranks.corr(dim_ranks, method='spearman')
                
                dimension_results[dim_num] = {
                    'scores': dim_scores.to_dict(),
                    'ranks': dim_ranks.to_dict()
                }
                correlations[dim_num] = correlation
                
                self.logger.info(f"Dimension {dim_num} correlation: {correlation:.4f}")
            
            return {
                "total_scores": total_scores.to_dict(),
                "total_ranks": total_ranks.to_dict(),
                "dimension_results": dimension_results,
                "correlations": correlations,
                "status": "success",
                "interpretation": self._get_interpretation(correlations)
            }

        except Exception as e:
            self.logger.error(f"Error in Construct Validity calculation: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    def _get_interpretation(self, correlations: Dict[str, float]) -> Dict[str, str]:
        """
        Get bilingual interpretation of correlation coefficients
        """
        interpretations = {}
        for dim, corr in correlations.items():
            if corr > 0.7:
                interpretations[dim] = "Strong / قوي"
            elif corr > 0.5:
                interpretations[dim] = "Moderate / متوسط"
            elif corr > 0.3:
                interpretations[dim] = "Weak / ضعيف"
            else:
                interpretations[dim] = "Very Weak / ضعيف جداً"
        return interpretations