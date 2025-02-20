# src/core/analyzer.py
from .statistics import (
    calculate_cronbach_alpha,
    calculate_split_half_reliability,
    calculate_construct_validity,
    export_statistics
)
import pandas as pd
import os

class StatisticalAnalyzer:
    def __init__(self, data_file, questions, dimensions):
        self.data = pd.read_excel(data_file)
        self.questions = questions
        self.dimensions = dimensions
        
    def analyze_and_export(self, output_dir='output'):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_file = os.path.join(output_dir, 'statistical_analysis.xlsx')
        export_statistics(output_file, self.data, self.questions, self.dimensions)
        return output_file