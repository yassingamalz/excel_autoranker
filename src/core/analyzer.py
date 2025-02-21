# src/core/analyzer.py
from .statistics_manager import StatisticsManager
from ..utils.logger import AppLogger
import pandas as pd
import os

class StatisticalAnalyzer:
    def __init__(self, data_file, selected_columns, dimensions):
        self.logger = AppLogger.get_logger()
        self.logger.info(f"Initializing StatisticalAnalyzer with {data_file}")
        
        # Log initial inputs
        self.logger.info("\n" + "="*80)
        self.logger.info("INPUT PARAMETERS")
        self.logger.info(f"Selected columns range: {selected_columns[0]} -> {selected_columns[-1]}")
        self.logger.info(f"Raw dimensions data: {dimensions}")
        self.logger.info("="*80)
        
        try:
            # Read Excel file
            xl = pd.ExcelFile(data_file)
            sheet_name = xl.sheet_names[0]
            self.data = pd.read_excel(data_file, sheet_name=sheet_name)
            self.logger.info(f"Successfully loaded data: {len(self.data)} rows, {len(self.data.columns)} columns")
            
            # Map questions based on selected range
            first_question_col = selected_columns[0]
            last_question_col = selected_columns[-1]
            self.questions = [self.data.columns[i] for i in range(first_question_col, last_question_col + 1)]
            
            # Process dimensions - Map column indices to actual column names
            self.dimensions = {}
            sorted_dim_nums = sorted(dimensions.keys())
            
            self.logger.info("\n" + "="*80)
            self.logger.info("DIMENSIONS MAPPING DETAILS")
            self.logger.info(f"Total number of dimensions to process: {len(sorted_dim_nums)}")
            self.logger.info("="*80)
            
            # Track last processed index
            last_index = first_question_col
            
            for i, dim_num in enumerate(sorted_dim_nums):
                self.logger.info("\n" + "-"*80)
                self.logger.info(f"DIMENSION {dim_num} ({i+1}/{len(sorted_dim_nums)})")
                
                if i < len(sorted_dim_nums) - 1:
                    # Check if we need to skip to next sequence start
                    current_indices = dimensions[dim_num]
                    if current_indices[0] > last_index:
                        self.logger.info(f"Skipping gap from {last_index} to {current_indices[0]}")
                        last_index = current_indices[0]
                    col_indices = [idx for idx in range(last_index, current_indices[-1] + 1)]
                    last_index = current_indices[-1] + 1
                else:
                    # Last dimension takes all remaining columns
                    col_indices = list(range(last_index, last_question_col + 1))
                
                self.logger.info(f"Processing indices: {','.join(map(str, col_indices))}")
                dim_cols = [self.data.columns[idx] for idx in col_indices if idx < len(self.data.columns)]
                
                if dim_cols:
                    self.dimensions[dim_num] = dim_cols
                    self.logger.info(f"Column names ({len(dim_cols)}): {','.join(dim_cols)}")
                else:
                    self.logger.warning(f"No valid columns found")
                
                self.logger.info("-"*80)
            
            # Verify mapping
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