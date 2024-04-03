import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import whois
import datetime

# Function to extract features from a URL
def extract_features(url):
    features = {}
    
    # Extract domain information
    domain = urlparse(url).hostname
    features['domain'] = domain
    
    try:
        whois_info = whois.whois(domain)
        creation_date = whois_info.creation_date
        expiration_date = whois_info.expiration_date
        age = (datetime.datetime.now() - creation_date).days
        features['domain_age'] = age
        features['domain_expiration'] = (expiration_date - datetime.datetime.now()).days
    except:
        features['domain_age'] = -1
        features['domain_expiration'] = -1
    
    # Extract URL-based features
    features['has_ip'] = bool(re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url))
    features['has_at'] = '@' in url
    features['url_length'] = len(url)
    
    # Fetch HTML content and extract features
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract form-related features
        forms = soup.find_all('form')
        features['form_count'] = len(forms)
        
        # Extract link-related features
        links = soup.find_all('a')
        features['link_count'] = len(links)
        
        # Extract script-related features
        scripts = soup.find_all('script')
        features['script_count'] = len(scripts)
        
        # Extract other HTML features
        features['has_iframe'] = bool(soup.find('iframe'))
        features['has_images'] = bool(soup.find('img'))
    except:
        pass
    
    return features

# Example usage
url = "https://example.com"
features = extract_features(url)
print(features)
