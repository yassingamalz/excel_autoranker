# src/core/analyzer.py
from .statistics import (
    calculate_cronbach_alpha,
    calculate_split_half_reliability,
    calculate_construct_validity,
    export_statistics
)
from ..utils.logger import AppLogger
import pandas as pd
import os

class StatisticalAnalyzer:
    def __init__(self, data_file, selected_columns, dimensions):
        self.logger = AppLogger.get_logger()
        self.logger.info(f"Initializing StatisticalAnalyzer with {data_file}")
        self.logger.debug(f"Selected columns: {selected_columns}")
        self.logger.debug(f"Dimensions: {dimensions}")
        
        try:
            # Read Excel file with explicit sheet name handling
            xl = pd.ExcelFile(data_file)
            self.logger.debug(f"Available sheets: {xl.sheet_names}")
            
            # Use first sheet by default
            sheet_name = xl.sheet_names[0]
            self.logger.info(f"Reading from sheet: {sheet_name}")
            
            self.data = pd.read_excel(data_file, sheet_name=sheet_name)
            self.logger.info(f"Successfully loaded data with {len(self.data)} rows")
            self.logger.debug(f"Column names: {list(self.data.columns)}")
            
            # Convert column indices to column names
            self.questions = [self.data.columns[i] for i in selected_columns]
            self.logger.debug(f"Mapped column names: {self.questions}")
            
            # Convert dimension indices to column names
            self.dimensions = {}
            for dim_name, col_indices in dimensions.items():
                dim_cols = [self.data.columns[i] for i in col_indices]
                self.dimensions[dim_name] = dim_cols
                self.logger.debug(f"Dimension {dim_name} columns: {dim_cols}")
                
        except Exception as e:
            self.logger.error(f"Error initializing analyzer: {str(e)}")
            self.logger.error("Full error details:", exc_info=True)
            raise
        
    def analyze_and_export(self, output_dir='output'):
        try:
            self.logger.info("Starting analysis")
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.logger.debug(f"Created output directory: {output_dir}")
            
            output_file = os.path.join(output_dir, 'statistical_analysis.xlsx')
            self.logger.info(f"Exporting analysis to: {output_file}")
            
            # Clean data before analysis
            self.clean_data()
            
            # Log data shape before export
            self.logger.debug(f"Data shape before export: {self.data.shape}")
            self.logger.debug(f"First few questions: {self.questions[:5]}")
            self.logger.debug("Sample of first few rows:")
            self.logger.debug(self.data[self.questions[:5]].head().to_string())
            
            export_statistics(output_file, self.data, self.questions, self.dimensions)
            self.logger.info("Analysis completed successfully")
            
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            self.logger.error("Full error details:", exc_info=True)
            raise
            
    def clean_data(self):
        """Clean and prepare data for analysis"""
        try:
            self.logger.info("Starting data cleaning")
            
            self.logger.debug(f"Data shape before cleaning: {self.data.shape}")
            self.logger.debug(f"Column dtypes before cleaning: {self.data.dtypes}")
            
            # Skip first row (titles) and reset index
            self.data = self.data.iloc[1:].reset_index(drop=True)
            self.logger.debug(f"Data shape after skipping first row: {self.data.shape}")
            
            # Convert Arabic text responses to numerical values
            mapping = {
                'مكتسبة بشكل كامل': 3,
                'مكتسبة بدرجة متوسطة': 2,
                'غير مكتسبة': 1
            }
            
            for col in self.questions:
                if self.data[col].dtype == 'object':
                    self.logger.debug(f"Converting text responses in column: {col}")
                    self.logger.debug(f"Unique values before mapping: {self.data[col].unique()}")
                    self.data[col] = self.data[col].map(mapping)
                    self.logger.debug(f"Unique values after mapping: {self.data[col].unique()}")
            
            self.logger.info("Data cleaning completed")
            self.logger.debug(f"Final data shape: {self.data.shape}")
            self.logger.debug(f"Final column dtypes: {self.data.dtypes}")
            
        except Exception as e:
            self.logger.error(f"Error during data cleaning: {str(e)}")
            self.logger.error("Full error details:", exc_info=True)
            raise