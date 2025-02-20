# src/core/statistics.py
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

def calculate_cronbach_alpha(data, questions):
    df = data[questions].apply(pd.to_numeric, errors='coerce')
    total_scores = df.sum(axis=1)
    question_variances = df.var()
    total_variance = total_scores.var()
    n_items = len(questions)
    cronbach_alpha = (n_items / (n_items - 1)) * (1 - question_variances.sum() / total_variance)
    
    return {
        'alpha': cronbach_alpha,
        'n_items': n_items,
        'question_variances': question_variances,
        'sum_variances': question_variances.sum(),
        'total_variance': total_variance,
        'total_scores': total_scores
    }

def calculate_split_half_reliability(data, questions):
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
    df = data[questions].apply(pd.to_numeric, errors='coerce')
    
    # Calculate total scores
    total_scores = df.sum(axis=1)
    total_ranks = total_scores.rank(method='average')
    
    # Calculate dimension scores and correlations
    dimension_stats = {}
    for dim_name, dim_questions in dimensions.items():
        dim_scores = data[dim_questions].apply(pd.to_numeric, errors='coerce').sum(axis=1)
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
    ws.title = "Statistical Analysis / التحليل الإحصائي"
    
    # Cronbach's Alpha
    alpha_stats = calculate_cronbach_alpha(data, questions)
    row = 1
    ws['A1'] = "Cronbach's Alpha / معامل ألفا كرونباخ"
    ws['A1'].font = Font(bold=True, size=14)
    
    # Split-Half Reliability
    split_half_stats = calculate_split_half_reliability(data, questions)
    row = len(dimensions) + 7
    ws[f'A{row}'] = "Split-Half Reliability / ثبات التجزئة النصفية"
    ws[f'A{row}'].font = Font(bold=True, size=14)
    row += 1
    ws[f'A{row}'] = "Pearson Correlation / معامل ارتباط بيرسون"
    ws[f'B{row}'] = split_half_stats['pearson_correlation']
    row += 1
    ws[f'A{row}'] = "Spearman-Brown Coefficient / معامل سبيرمان-براون"
    ws[f'B{row}'] = split_half_stats['spearman_brown']
    
    # Construct Validity
    construct_stats = calculate_construct_validity(data, questions, dimensions)
    row += 2
    ws[f'A{row}'] = "Construct Validity / صدق البناء"
    ws[f'A{row}'].font = Font(bold=True, size=14)
    row += 1
    
    for dim_name, stats in construct_stats['dimensions'].items():
        ws[f'A{row}'] = f"Dimension {dim_name} / البعد {dim_name}"
        ws[f'B{row}'] = stats['correlation']
        row += 1
    
    wb.save(filepath)