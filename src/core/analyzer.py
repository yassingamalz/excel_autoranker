# src/core/analyzer.py
from .statistics_manager import StatisticsManager
from ..utils.logger import AppLogger
import pandas as pd
import os

class StatisticalAnalyzer:
    def __init__(self, data_file, selected_columns, dimensions):
        self.logger = AppLogger.get_logger()
        self.logger.info(f"Initializing StatisticalAnalyzer with {data_file}")
        self.logger.debug(f"Selected columns: {selected_columns}")
        self.logger.debug(f"Dimensions data received: {dimensions}")
        
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
            last_question_col = selected_columns[-1]
            self.logger.debug(f"First question column index: {first_question_col}")
            self.logger.debug(f"Last question column index: {last_question_col}")
            
            # Convert column indices to column names, starting from the first selected column
            self.questions = [self.data.columns[i] for i in range(first_question_col, last_question_col + 1)]
            self.logger.debug(f"Total question columns mapped: {len(self.questions)}")
            
            # Process dimensions - Map column indices to actual column names
            self.dimensions = {}
            sorted_dim_nums = sorted(dimensions.keys())
            self.logger.info(f"Processing {len(sorted_dim_nums)} dimensions")
            
            for i, dim_num in enumerate(sorted_dim_nums):
                self.logger.debug(f"Processing dimension {dim_num} ({i+1} of {len(sorted_dim_nums)})")
                
                if i < len(sorted_dim_nums) - 1:
                    # Handle regular dimensions
                    col_indices = dimensions[dim_num]
                    self.logger.debug(f"Dimension {dim_num} original indices: {col_indices}")
                else:
                    # Handle last dimension
                    prev_dim = sorted_dim_nums[i-1]
                    start_idx = dimensions[prev_dim][-1] + 1
                    self.logger.debug(f"Last dimension {dim_num} starts at index {start_idx}")
                    col_indices = list(range(start_idx, last_question_col + 1))
                    self.logger.debug(f"Last dimension {dim_num} indices: {col_indices}")
                
                # Map indices to column names
                dim_cols = [self.data.columns[idx] for idx in col_indices if idx < len(self.data.columns)]
                
                if dim_cols:
                    self.dimensions[dim_num] = dim_cols
                    self.logger.info(f"Dimension {dim_num} mapped to {len(dim_cols)} columns: {dim_cols}")
                else:
                    self.logger.warning(f"Dimension {dim_num} has no valid columns")
            
            # Verify all questions are assigned to dimensions
            total_dim_cols = sum(len(cols) for cols in self.dimensions.values())
            self.logger.info(f"Total columns in dimensions: {total_dim_cols}")
            self.logger.info(f"Total question columns: {len(self.questions)}")
            if total_dim_cols != len(self.questions):
                self.logger.warning("Mismatch between dimension columns and total questions")
            
        except Exception as e:
            self.logger.error(f"Error initializing analyzer: {str(e)}")
            self.logger.error("Full error details:", exc_info=True)
            raise
       
    def analyze_and_export(self, output_dir='/app/data/output'):
        try:
            self.logger.info("Starting analysis")
            self.logger.debug(f"Ensuring output directory: {output_dir}")
            
            # Clean data before analysis
            self.clean_data()
            
            # Create statistics manager and run analysis
            self.logger.info("Creating statistics manager")
            self.logger.debug(f"Passing {len(self.questions)} questions and {len(self.dimensions)} dimensions")
            stats_manager = StatisticsManager(self.data, self.questions, self.dimensions)
            output_file = stats_manager.analyze_and_export(output_dir)
            
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