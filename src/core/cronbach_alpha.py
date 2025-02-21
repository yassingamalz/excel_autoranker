# src/core/cronbach_alpha.py
import pandas as pd
import logging
from typing import Dict

class CronbachAlphaCalculator:
    @staticmethod
    def calculate(data: pd.DataFrame, questions: list, logger: logging.Logger = None) -> Dict:
        if logger is None:
            logger = logging.getLogger(__name__)
        
        logger.info("Starting Cronbach's Alpha calculation")
        try:
            df = data[questions].apply(pd.to_numeric, errors='coerce').dropna()
            
            if len(df.columns) < 2:
                logger.error("Insufficient questions for reliability analysis")
                return {"alpha": None, "valid_questions": len(df.columns)}
            
            n = len(df.columns)
            variances = df.var()
            total_scores = df.sum(axis=1)
            total_variance = total_scores.var()
            
            if total_variance == 0:
                logger.warning("Total variance is zero - cannot compute alpha")
                return {"alpha": 0.0, "valid_questions": n}
            
            alpha = (n / (n - 1)) * (1 - (variances.sum() / total_variance))
            logger.info(f"Cronbach's Alpha calculated: {alpha:.4f}")
            
            return {
                "alpha": alpha,
                "valid_questions": n,
                "variances": variances.to_dict(),
                "total_variance": total_variance
            }
        
        except Exception as e:
            logger.error(f"Error in alpha calculation: {str(e)}")
            return {"alpha": None, "error": str(e)}