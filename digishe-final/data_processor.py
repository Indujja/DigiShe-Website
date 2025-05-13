import pandas as pd
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_scheme_name(name):
    """Clean scheme names to remove unwanted text"""
    # Remove text in parentheses
    name = re.sub(r'\([^)]*\)', '', name)
    
    # Remove trailing punctuation and spaces
    name = name.strip('., \t\n\r')
    
    return name.strip()

def is_women_related(scheme_name):
    """Check if a scheme is women-related based on keywords"""
    keywords = ['women', 'woman', 'girl', 'female', 'mother', 'maternity', 
                'pregnancy', 'pregnant', 'widow', 'lady', 'ladies', 
                'mahila', 'stree', 'nari', 'mahila', 'beti', 'daughter']
    
    scheme_name_lower = scheme_name.lower()
    return any(keyword in scheme_name_lower for keyword in keywords)

def categorize_scheme(scheme_name):
    """Categorize schemes into different types based on keywords"""
    scheme_name_lower = scheme_name.lower()
    
    # Define categories and their keywords
    categories = {
        'Education': ['education', 'school', 'college', 'university', 'student', 'study', 
                     'academic', 'learning', 'educational'],
        'Scholarship': ['scholarship', 'fellowship', 'stipend', 'grant', 'award', 'financial aid'],
        'Health': ['health', 'medical', 'healthcare', 'hospital', 'medicine', 'maternity', 
                  'pregnancy', 'pregnant', 'nutrition', 'care', 'clinic'],
        'Employment': ['employment', 'job', 'work', 'career', 'skill', 'training', 
                      'entrepreneur', 'business', 'livelihood', 'profession', 'vocational'],
        'Safety': ['safety', 'protection', 'security', 'shelter', 'rescue', 'violence', 
                  'abuse', 'harassment', 'helpline'],
        'Legal': ['legal', 'law', 'rights', 'justice', 'court', 'divorce', 'alimony', 
                 'custody', 'property'],
        'Child Welfare': ['child', 'children', 'infant', 'baby', 'kid', 'toddler', 
                         'adolescent', 'juvenile', 'creche', 'daycare'],
    }
    
    # Check each category
    for category, keywords in categories.items():
        if any(keyword in scheme_name_lower for keyword in keywords):
            return category
    
    # Default category if no matches
    return 'General'

def process_data(filepath):
    """Process the CSV file to get clean, filtered government schemes data"""
    try:
        # Read the CSV file
        df = pd.read_csv(filepath)
        
        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        
        # Ensure required columns exist
        required_columns = ['Scheme Name', 'URL']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Required column '{col}' not found in data")
                return []
        
        # Clean scheme names
        df['Scheme Name'] = df['Scheme Name'].apply(clean_scheme_name)
        
        # Filter for women-related schemes
        df = df[df['Scheme Name'].apply(is_women_related)]
        
        # Add category to each scheme
        df['Category'] = df['Scheme Name'].apply(categorize_scheme)
        
        # Convert to list of dictionaries for easier handling in Flask
        schemes = df.to_dict('records')
        
        return schemes
    
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return []