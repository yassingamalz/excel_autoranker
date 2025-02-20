import os
import pandas as pd
from ..dialogs.error_dialog import ErrorDialog

def validate_excel_file(file_path):
    """
    Validate that the selected file is a valid Excel file.
    """
    if not os.path.exists(file_path):
        ErrorDialog.show_error("File Error", "Selected file does not exist.")
        return False
        
    try:
        # Try to read the Excel file
        df = pd.read_excel(file_path)
        
        # Check if file has any data
        if df.empty:
            ErrorDialog.show_error("File Error", "Selected Excel file is empty.")
            return False
            
        return True
        
    except Exception as e:
        ErrorDialog.show_error("File Error", f"Error reading Excel file: {str(e)}")
        return False