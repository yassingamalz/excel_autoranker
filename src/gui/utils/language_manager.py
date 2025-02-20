from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import Qt

class LanguageManager:
    TRANSLATIONS = {
        'en': {
            'app_title': "Excel AutoRanker",
            'file_select': "Select Excel File",
            'no_file': "No file selected",
            'dimensions': "Number of Dimensions",
            'configure_dims': "Configure Dimensions",
            'data_cleaning': "Data Cleaning Options",
            'needs_cleaning': "Data needs cleaning",
            'run_analysis': "Run Analysis",
            'export_excel': "Export to Excel",
            'export_word': "Export to Word",
        },
        'ar': {
            'app_title': "التصنيف التلقائي للإكسل",
            'file_select': "اختر ملف إكسل",
            'no_file': "لم يتم اختيار ملف",
            'dimensions': "عدد الأبعاد",
            'configure_dims': "تكوين الأبعاد",
            'data_cleaning': "خيارات تنظيف البيانات",
            'needs_cleaning': "البيانات تحتاج إلى تنظيف",
            'run_analysis': "تشغيل التحليل",
            'export_excel': "تصدير إلى إكسل",
            'export_word': "تصدير إلى وورد",
        }
    }
    
    @staticmethod
    def get_text(key, lang='en'):
        return f"{LanguageManager.TRANSLATIONS['en'][key]} / {LanguageManager.TRANSLATIONS['ar'][key]}"
