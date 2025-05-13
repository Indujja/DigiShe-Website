from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import logging
from data_processor import process_data
from app import check_urls_in_background, search_schemes, sort_schemes_by_validity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load and process data
schemes_data = process_data('data/schemes.csv')

# Translations for multilingual support
translations = {
    'en': {
        'home': 'Home',
        'schemes': 'Schemes',
        'about': 'About',
        'contact': 'Contact',
        'search_placeholder': 'Search for schemes...',
        'search_button': 'Search',
        'visit_website': 'Visit Website',
        'no_results': 'No schemes found matching your search.',
        'footer_text': 'DigiShe provides a comprehensive directory of government schemes for women empowerment and welfare.'
    },
    'kn': {
        'home': 'ಮುಖಪುಟ',
        'schemes': 'ಯೋಜನೆಗಳು',
        'about': 'ನಮ್ಮ ಬಗ್ಗೆ',
        'contact': 'ಸಂಪರ್ಕಿಸಿ',
        'search_placeholder': 'ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ...',
        'search_button': 'ಹುಡುಕಿ',
        'visit_website': 'ವೆಬ್‌ಸೈಟ್‌ಗೆ ಭೇಟಿ ನೀಡಿ',
        'no_results': 'ನಿಮ್ಮ ಹುಡುಕಾಟಕ್ಕೆ ಹೊಂದಿಕೆಯಾಗುವ ಯಾವುದೇ ಯೋಜನೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ.',
        'footer_text': 'DigiShe ಮಹಿಳಾ ಸಬಲೀಕರಣ ಮತ್ತು ಕಲ್ಯಾಣಕ್ಕಾಗಿ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಸಮಗ್ರ ಡೈರೆಕ್ಟರಿಯನ್ನು ಒದಗಿಸುತ್ತದೆ.'
    }
}

@app.route('/')
def index():
    # Get language preference
    lang = request.args.get('lang', 'en')
    if lang not in translations:
        lang = 'en'
    
    return render_template('index.html', 
                           current_lang=lang, 
                           translations=translations[lang])

@app.route('/schemes')
def schemes():
    # Get language preference
    lang = request.args.get('lang', 'en')
    if lang not in translations:
        lang = 'en'
    
    # Get search query if any
    query = request.args.get('query', '')
    
    # Filter schemes based on search query
    filtered_schemes = schemes_data
    if query:
        filtered_schemes = search_schemes(filtered_schemes, query)
    
    # Sort schemes to show valid URLs first
    sorted_schemes = sort_schemes_by_validity(filtered_schemes)
    
    return render_template('schemes.html', 
                           schemes=sorted_schemes, 
                           current_lang=lang, 
                           translations=translations[lang],
                           search_query=query)

@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query', '')
    lang = request.args.get('lang', 'en')
    
    if not query:
        return jsonify([])
    
    filtered_schemes = search_schemes(schemes_data, query)
    sorted_schemes = sort_schemes_by_validity(filtered_schemes)
    
    return jsonify(sorted_schemes)

if __name__ == '__main__':
    # Start URL validity check in background
    check_urls_in_background(schemes_data)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)