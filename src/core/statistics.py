import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

def calculate_cronbach_alpha(data, questions):
    """
    Detailed Cronbach's Alpha calculation
    
    :param data: DataFrame containing the data
    :param questions: List of question column names
    :return: Dictionary with detailed Cronbach's Alpha calculation components
    """
    # Select only the specified questions and convert to numeric
    df = data[questions].apply(pd.to_numeric, errors='coerce')
    
    # حساب تباين كل سؤال - Variance of each question
    question_variances = df.var()
    
    # مجموع تباينات الأسئلة - Sum of question variances
    sum_question_variances = question_variances.sum()
    
    # حساب المجموع الكلي لكل مشارك - Total score for each participant
    total_scores = df.sum(axis=1)
    
    # تباين المجموع الكلي - Variance of total scores
    total_variance = total_scores.var()
    
    # Number of questions
    n_items = len(questions)
    
    # Cronbach's Alpha calculation
    cronbach_alpha = (n_items / (n_items - 1)) * (1 - (sum_question_variances / total_variance))
    
    return {
        'n_items': n_items,
        'question_variances': question_variances,
        'sum_question_variances': sum_question_variances,
        'total_scores': total_scores,
        'total_variance': total_variance,
        'cronbach_alpha': cronbach_alpha
    }

def calculate_split_half_reliability(data, questions):
    """
    Calculate split-half reliability
    
    :param data: DataFrame containing the data
    :param questions: List of question column names
    :return: Dictionary with split-half reliability metrics
    """
    df = data[questions].apply(pd.to_numeric, errors='coerce')
    
    # Split questions into odd and even
    odd_questions = questions[::2]
    even_questions = questions[1::2]
    
    # Calculate sums for odd and even questions
    odd_sums = df[odd_questions].sum(axis=1)
    even_sums = df[even_questions].sum(axis=1)
    
    # Calculate Pearson correlation
    pearson_corr = odd_sums.corr(even_sums)
    
    # Calculate Spearman-Brown coefficient
    spearman_brown = (2 * pearson_corr) / (1 + pearson_corr)
    
    return {
        'pearson_correlation': pearson_corr,
        'spearman_brown': spearman_brown,
        'odd_sums': odd_sums,
        'even_sums': even_sums
    }

def calculate_construct_validity(data, questions, dimensions):
    """
    Calculate construct validity for dimensions
    
    :param data: DataFrame containing the data
    :param questions: List of question column names
    :param dimensions: Dictionary of dimensions with their questions
    :return: Dictionary with construct validity metrics
    """
    df = data[questions].apply(pd.to_numeric, errors='coerce')
    
    # Calculate total scores
    total_scores = df.sum(axis=1)
    total_ranks = total_scores.rank(method='average')
    
    # Calculate dimension scores and correlations
    dimension_stats = {}
    for dim_name, dim_questions in dimensions.items():
        # Ensure dim_questions are in the correct order and exist in the data
        valid_dim_questions = [q for q in dim_questions if q in data.columns]
        
        dim_scores = data[valid_dim_questions].apply(pd.to_numeric, errors='coerce').sum(axis=1)
        dim_ranks = dim_scores.rank(method='average')
        correlation = total_ranks.corr(dim_ranks, method='spearman')
        
        dimension_stats[dim_name] = {
            'scores': dim_scores,
            'ranks': dim_ranks,
            'correlation': correlation
        }
    
    return {
        'total_scores': total_scores,
        'total_ranks': total_ranks,
        'dimensions': dimension_stats
    }

def export_statistics(filepath, data, questions, dimensions):
    """
    Export statistical analysis to Excel
    
    :param filepath: Path to save the Excel file
    :param data: DataFrame containing the data
    :param questions: List of question column names
    :param dimensions: Dictionary of dimensions with their questions
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Statistical_Analysis"
    
    # Cronbach's Alpha Calculation
    alpha_stats = calculate_cronbach_alpha(data, questions)
    
    # Styling
    header_font = Font(bold=True, size=14)
    subheader_font = Font(bold=True)
    
    # Main Title
    ws['A1'] = "Cronbach's Alpha / معامل ألفا كرونباخ"
    ws['A1'].font = header_font
    
    # Detailed Breakdown Headers
    headers = [
        "عدد الأسئلة (N of Items)", 
        "مجموع تباينات الأسئلة (Sum of Question Variances)", 
        "تباين المجموع الكلي (Total Score Variance)", 
        "معامل ألفا كرونباخ (Cronbach's Alpha)"
    ]
    
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = subheader_font
    
    # Fill in Cronbach's Alpha values
    ws.cell(row=4, column=1, value=alpha_stats['n_items'])
    ws.cell(row=4, column=2, value=alpha_stats['sum_question_variances'])
    ws.cell(row=4, column=3, value=alpha_stats['total_variance'])
    ws.cell(row=4, column=4, value=alpha_stats['cronbach_alpha'])
    
    # Individual Question Variances
    ws['A6'] = "تباين كل سؤال (Individual Question Variances)"
    ws['A6'].font = subheader_font
    
    for idx, (question, variance) in enumerate(alpha_stats['question_variances'].items(), start=7):
        ws.cell(row=idx, column=1, value=question)
        ws.cell(row=idx, column=2, value=variance)
    
    wb.save(filepath)