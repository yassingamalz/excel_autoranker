# Excel AutoRanker: Statistical Analysis Automation Tool 📊🏆

## Project Structure
```
excel_autoranker/
├── src/
│   ├── gui/          # Graphical user interface components
│   │   ├── components/
│   │   │   ├── file_selector.py
│   │   │   ├── question_range_selector.py
│   │   │   ├── dimension_config.py
│   │   │   ├── data_cleaner.py
│   │   │   └── progress_indicator.py
│   │   ├── dialogs/
│   │   │   ├── dimension_popup.py
│   │   │   ├── config_popup.py
│   │   │   └── error_dialog.py
│   │   ├── layouts/
│   │   │   ├── main_layout.py
│   │   │   └── analysis_layout.py
│   │   ├── utils/
│   │   │   ├── validators.py
│   │   │   └── styles.py
│   │   ├── assets/
│   │   ├── __init__.py
│   │   └── main_window.py
│   ├── core/         # Core data processing functionality
│   ├── statistical/  # Statistical analysis implementations
│   ├── reports/      # Report generation modules
│   └── utils/        # Utility functions and helpers
├── config/           # Configuration files
├── resources/
│   ├── templates/    # Report templates
│   └── mappings/     # Data mapping configurations
├── tests/
│   ├── unit/        # Unit tests
│   └── integration/ # Integration tests
├── docker/          # Docker-related files
├── docs/
│   ├── user_guide/  # End-user documentation
│   └── technical/   # Technical documentation
├── data/
│   ├── input/       # Input data directory
│   └── output/      # Generated reports directory
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── Dockerfile
└── docker-compose.yml
```

## Project Overview
Excel AutoRanker is an automated ranking and statistical analysis tool specifically designed to process questionnaire-based Excel files through an intuitive graphical interface.

## Core User Interaction Flow

### 1. Data Selection and Configuration
- Interactive question range selection within the dataset
- Popup interface for:
  - Specifying the total number of dimensions
  - Selecting question ranges for each dimension
- Data cleaning configuration:
  - Option to process raw or pre-cleaned data
  - Arabic text to numerical value mapping:
    - `مكتسبة بشكل كامل = 3` (Fully Acquired)
    - `مكتسبة بدرجة متوسطة = 2` (Moderately Acquired)
    - `غير مكتسبة = 1` (Not Acquired)

### 2. Statistical Analysis Components
- Reliability Analysis
  - Full test Cronbach's Alpha (α) calculation
  - Dimension-specific Spearman-Brown split-half coefficients
- Correlation Analysis
  - Per-dimension Spearman's rank correlation
  - Cross-dimensional correlation metrics
- Detailed Statistics
  - Question-level statistical analysis within dimensions 
  - Comprehensive scoring metrics
- Automated Ranking
  - Score calculation and normalization
  - Sophisticated tie-breaking mechanism

### 3. Report Generation
- Excel Output
  - Multiple detailed analysis sheets
  - Dimensional breakdowns
  - Statistical summaries
- Word Report
  - Formatted analysis presentation
  - Data visualizations
  - Statistical interpretations

## Technical Implementation

### User Interface Development
- Graphical Interface Components
  - Excel file selection dialog
  - Question range selector
  - Dimension configuration popup
  - Data cleaning options panel
  - Analysis progress indicators

### Data Processing Engine
- Input Handling
  - Excel file reading (.xlsx, .xls)
  - Data validation and structure verification
- Arabic Text Processing
  - Custom value mapping system
  - Text-to-numerical conversion
  - Data cleaning automation

### Statistical Module
- Reliability Metrics
  - Overall Cronbach's Alpha implementation
  - Split-half reliability calculation
- Correlation Analysis
  - Spearman's rank correlation engine
  - Multi-dimensional analysis system
- Ranking System
  - Score normalization
  - Tie detection and resolution
  - Rank assignment logic

### Deployment System
- Docker Configuration
  - Container setup and configuration
  - Volume mapping for data access
  - Cross-platform compatibility
- Command Line Interface
  ```sh
  docker build -t excel_autoranker .
  docker run --rm -v $(pwd)/data:/app/data excel_autoranker
  ```

## Development Phases

### Phase 1: Core Foundation
1. User interface skeleton
2. Basic data processing
3. Initial Arabic text handling

### Phase 2: Statistical Implementation
1. Reliability analysis systems
2. Correlation calculations
3. Ranking mechanism

### Phase 3: Interface Enhancement
1. Interactive components
2. Data validation
3. Progress feedback

### Phase 4: Output Generation
1. Excel report formatting
2. Word document creation
3. Visual representations

### Phase 5: Deployment & Testing
1. Docker implementation
2. System testing
3. User documentation

## Quality Control
- Comprehensive testing
  - Statistical accuracy verification
  - Arabic text processing validation
  - User interface testing
- Performance optimization
- Error handling

## Future Enhancements
- Additional statistical methods
- Enhanced visualization options
- Batch processing capabilities
- Multi-language support
- API integration

## Support
- User documentation
- Technical troubleshooting
- Regular updates
- Bug tracking system