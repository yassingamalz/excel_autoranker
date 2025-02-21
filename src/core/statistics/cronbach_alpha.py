# src/core/statistics/cronbach_alpha.py
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os
from typing import Dict, List

class CronbachAlphaCalculator:
    def __init__(self):
        self._setup_logger()
        
    def _setup_logger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        self.logger = logging.getLogger('CronbachAlpha')
        self.logger.setLevel(logging.DEBUG)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/cronbach_alpha_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)

    def calculate(self, data: pd.DataFrame, questions: List[str]) -> Dict:
        """
        Calculate Cronbach's Alpha for given questions
        """
        self.logger.info(f"Starting Cronbach's Alpha calculation for {len(questions)} questions")
        self.logger.debug(f"Question columns: {questions}")

        try:
            # Convert to numeric and handle missing values
            df = data[questions].apply(pd.to_numeric, errors='coerce')
            df_clean = df.dropna()
            
            self.logger.debug(f"Data shape after cleaning: {df_clean.shape}")
            
            n_items = len(questions)
            if n_items < 2:
                self.logger.warning("Insufficient items for reliability analysis")
                return {
                    "alpha": None,
                    "n_items": n_items,
                    "status": "error",
                    "message": "Insufficient items for analysis"
                }

            # Calculate variances
            item_variances = df_clean.var()
            total_scores = df_clean.sum(axis=1)
            total_variance = total_scores.var()

            self.logger.debug(f"Item variances: {item_variances.to_dict()}")
            self.logger.debug(f"Total variance: {total_variance}")

            if total_variance == 0:
                self.logger.warning("Total variance is zero")
                return {
                    "alpha": 0.0,
                    "n_items": n_items,
                    "status": "error",
                    "message": "Zero total variance"
                }

            # Calculate alpha
            alpha = (n_items / (n_items - 1)) * (1 - (item_variances.sum() / total_variance))
            
            self.logger.info(f"Successfully calculated Cronbach's Alpha: {alpha:.4f}")
            
            return {
                "alpha": alpha,
                "n_items": n_items,
                "item_variances": item_variances.to_dict(),
                "total_variance": total_variance,
                "status": "success",
                "interpretation": self._get_interpretation(alpha)
            }

        except Exception as e:
            self.logger.error(f"Error in alpha calculation: {str(e)}", exc_info=True)
            return {
                "alpha": None,
                "n_items": len(questions),
                "status": "error",
                "message": str(e)
            }

    def _get_interpretation(self, alpha: float) -> str:
        """
        Get bilingual interpretation of alpha value
        """
        if alpha > 0.9:
            return "Excellent / ممتاز"
        elif alpha > 0.8:
            return "Good / جيد"
        elif alpha > 0.7:
            return "Acceptable / مقبول"
        else:
            return "Poor / ضعيف"