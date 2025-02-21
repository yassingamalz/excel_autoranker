# src/core/statistics/split_half.py
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os
from typing import Dict, List

class SplitHalfCalculator:
    def __init__(self):
        self._setup_logger()
        
    def _setup_logger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        self.logger = logging.getLogger('SplitHalf')
        self.logger.setLevel(logging.DEBUG)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/split_half_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)

    def calculate(self, data: pd.DataFrame, questions: List[str]) -> Dict:
        """
        Calculate Split-Half reliability using odd-even method
        """
        self.logger.info(f"Starting Split-Half calculation for {len(questions)} questions")
        self.logger.debug(f"Question columns: {questions}")

        try:
            # Convert to numeric and handle missing values
            df = data[questions].apply(pd.to_numeric, errors='coerce')
            df_clean = df.dropna()
            
            self.logger.debug(f"Data shape after cleaning: {df_clean.shape}")
            
            # Split questions into odd and even
            odd_questions = questions[::2]  # Get items at odd indices (0, 2, 4, ...)
            even_questions = questions[1::2]  # Get items at even indices (1, 3, 5, ...)
            
            self.logger.debug(f"Odd questions: {odd_questions}")
            self.logger.debug(f"Even questions: {even_questions}")
            
            # Calculate sums for each participant
            odd_sums = df_clean[odd_questions].sum(axis=1)
            even_sums = df_clean[even_questions].sum(axis=1)
            
            # Calculate Pearson correlation
            pearson_corr = odd_sums.corr(even_sums)
            
            # Calculate Spearman-Brown coefficient
            spearman_brown = (2 * pearson_corr) / (1 + pearson_corr)
            
            self.logger.info(f"Successfully calculated Split-Half reliability:")
            self.logger.info(f"Pearson correlation: {pearson_corr:.4f}")
            self.logger.info(f"Spearman-Brown coefficient: {spearman_brown:.4f}")
            
            return {
                "odd_questions": odd_questions,
                "even_questions": even_questions,
                "pearson_correlation": pearson_corr,
                "spearman_brown": spearman_brown,
                "odd_sums": odd_sums.to_dict(),
                "even_sums": even_sums.to_dict(),
                "status": "success",
                "interpretation": self._get_interpretation(spearman_brown)
            }

        except Exception as e:
            self.logger.error(f"Error in Split-Half calculation: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    def _get_interpretation(self, coefficient: float) -> str:
        """
        Get bilingual interpretation of Split-Half reliability coefficient
        """
        if coefficient > 0.9:
            return "Excellent / ممتاز"
        elif coefficient > 0.8:
            return "Good / جيد"
        elif coefficient > 0.7:
            return "Acceptable / مقبول"
        else:
            return "Poor / ضعيف"