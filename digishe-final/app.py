import requests
import threading
import logging
import time
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_url(url):
    """Check if a URL is valid and accessible"""
    try:
        # Parse URL to ensure it has scheme
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = 'http://' + url
        
        # Try to access the URL with a timeout
        response = requests.head(url, timeout=5, allow_redirects=True, verify=True)
        return response.status_code < 400  # Return True for successful status codes
    except Exception as e:
        logger.info(f"Error checking URL {url}: {e}")
        return False

def check_urls_in_background(schemes):
    """Check all URLs in the dataset and update their validity status"""
    logger.info("Starting URL validity check in background...")
    
    def worker():
        for scheme in schemes:
            if 'URL' in scheme:
                url = scheme['URL']
                scheme['valid_url'] = check_url(url)
                time.sleep(0.2)  # Add small delay to prevent rate limiting
        
        logger.info("URL validity check completed.")
    
    # Start the check in a background thread
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

def search_schemes(schemes, query):
    """Search for schemes based on the query"""
    query = query.lower()
    results = []
    
    for scheme in schemes:
        scheme_name = scheme['Scheme Name'].lower()
        if query in scheme_name:
            results.append(scheme)
    
    return results

def sort_schemes_by_validity(schemes):
    """Sort schemes to show valid URLs first"""
    # Create a copy to avoid modifying the original data
    sorted_schemes = sorted(schemes, key=lambda x: x.get('valid_url', True), reverse=True)
    return sorted_schemes