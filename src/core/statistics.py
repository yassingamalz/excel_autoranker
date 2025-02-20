import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

def calculate_cronbach_alpha(data, questions):
    # Convert to numeric, ensuring all questions are processed
    df = data[questions].apply(pd.to_numeric, errors='coerce')
    
    # Number of items
    n_items = len(questions)
    
    # Individual question variances
    question_variances = df.var()
    
    # Sum of question variances
    sum_question_variances = question_variances.sum()
    
    # Total scores (sum of all questions for each participant)
    total_scores = df.sum(axis=1)
    
    # Total score variance
    total_variance = total_scores.var()
    
    # Cronbach's Alpha calculation
    # α = (k / (k-1)) * (1 - (Σs²ᵢ / s²ₜ))
    cronbach_alpha = (n_items / (n_items - 1)) * (1 - (sum_question_variances / total_variance))
    
    return {
        'n_items': n_items,
        'question_variances': question_variances,
        'sum_question_variances': sum_question_variances,
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
    wb = Workbook()
    ws = wb.active
    ws.title = "Statistical_Analysis"
    
    # Cronbach's Alpha Calculation
    alpha_stats = calculate_cronbach_alpha(data, questions)
    
    # Main Title
    ws['A1'] = "Cronbach's Alpha / معامل ألفا كرونباخ"
    ws['A1'].font = Font(bold=True, size=14)
    
    # Detailed Breakdown Headers
    headers = [
        "عدد الأسئلة (N of Items)", 
        "مجموع تباينات الأسئلة (Sum of Question Variances)", 
        "تباين المجموع الكلي (Total Score Variance)", 
        "معامل ألفا كرونباخ (Cronbach's Alpha)"
    ]
    
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = Font(bold=True)
    
    # Fill in Cronbach's Alpha values
    ws.cell(row=4, column=1, value=alpha_stats['n_items'])
    ws.cell(row=4, column=2, value=round(alpha_stats['sum_question_variances'], 5))
    ws.cell(row=4, column=3, value=round(alpha_stats['total_variance'], 5))
    ws.cell(row=4, column=4, value=round(alpha_stats['cronbach_alpha'], 6))
    
    # Individual Question Variances
    ws['A6'] = "تباين كل سؤال (Individual Question Variances)"
    ws['A6'].font = Font(bold=True)
    
    for idx, (question, variance) in enumerate(alpha_stats['question_variances'].items(), start=7):
        ws.cell(row=idx, column=1, value=question)
        ws.cell(row=idx, column=2, value=round(variance, 6))
    
    wb.save(filepath)
