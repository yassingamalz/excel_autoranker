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
           
           # Find the first question column
           first_question_col = selected_columns[0]
           
           # Convert column indices to column names, starting from the first selected column
           self.questions = [self.data.columns[i] for i in range(first_question_col, selected_columns[-1] + 1)]
           self.logger.debug(f"Mapped column names: {self.questions}")
           
           # Recalculate dimensions based on the first question column
           self.dimensions = {}
           current_start = first_question_col
           for dim_name, col_indices in dimensions.items():
               # Find the start and end of each dimension relative to the first question column
               dim_start = max(current_start, col_indices[0])
               dim_end = min(col_indices[-1], selected_columns[-1])
               
               # Select dimension columns
               dim_cols = [self.data.columns[i] for i in range(dim_start, dim_end + 1)]
               self.dimensions[dim_name] = dim_cols
               self.logger.debug(f"Dimension {dim_name} columns: {dim_cols}")
               
               # Update current start for next dimension
               current_start = dim_end + 1
               
       except Exception as e:
           self.logger.error(f"Error initializing analyzer: {str(e)}")
           self.logger.error("Full error details:", exc_info=True)
           raise
       
   def analyze_and_export(self, output_dir='/app/data/output'):
       try:
           self.logger.info("Starting analysis")
           
           # Ensure output directory exists
           os.makedirs(output_dir, exist_ok=True)
           self.logger.debug(f"Ensuring output directory: {output_dir}")
           
           output_file = os.path.join(output_dir, 'statistical_analysis.xlsx')
           self.logger.info(f"Exporting analysis to: {output_file}")
           
           # Clean data before analysis
           self.clean_data()
           
           export_statistics(output_file, self.data, self.questions, self.dimensions)
           self.logger.info("Analysis completed successfully")
           
           # Verify file exists
           if os.path.exists(output_file):
               self.logger.info(f"File successfully created: {output_file}")
               return output_file
           else:
               self.logger.error("File was not created")
               raise FileNotFoundError("Output file was not created")
           
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
           
           # Identify the header row
           def is_header_row(row):
               # Check if the row contains column-like text in question columns
               return any(
                   pd.isna(row[col]) or 
                   (isinstance(row[col], str) and (
                       row[col].strip() in ['', 'مكتسبة بشكل كامل', 'مكتسبة بدرجة متوسطة', 'غير مكتسبة']
                   )) 
                   for col in self.questions
               )
           
           # Find the first non-header row
           first_data_row = next((i for i in range(len(self.data)) if not is_header_row(self.data.iloc[i])), 0)
           
           # Slice the dataframe from the first non-header row
           self.data = self.data.iloc[first_data_row:].reset_index(drop=True)
           
           self.logger.debug(f"Data shape after identifying first data row: {self.data.shape}")
           
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