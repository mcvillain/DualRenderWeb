import os
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def fetch_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Update relative URLs to absolute URLs
        for tag in soup.find_all(['a', 'link', 'img', 'script']):
            if tag.has_attr('href'):
                tag['href'] = urljoin(url, tag['href'])
            if tag.has_attr('src'):
                tag['src'] = urljoin(url, tag['src'])
        
        return str(soup)
    except requests.RequestException as e:
        app.logger.error(f"Error fetching content: {str(e)}")
        return f"Error fetching content: {str(e)}"

@app.route('/')
def index():
    app.logger.info("Index route accessed")
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    app.logger.info("Fetch route accessed")
    url1 = request.form.get('url1')
    url2 = request.form.get('url2')
    
    if not url1 or not url2:
        app.logger.error("Both URLs are required")
        return jsonify({'error': 'Both URLs are required'}), 400
    
    if not urlparse(url1).scheme:
        url1 = 'http://' + url1
    if not urlparse(url2).scheme:
        url2 = 'http://' + url2
    
    app.logger.info(f"Fetching content from {url1} and {url2}")
    content1 = fetch_content(url1)
    content2 = fetch_content(url2)
    
    return jsonify({
        'content1': content1,
        'content2': content2
    })

@app.route('/test')
def test():
    app.logger.info("Test route accessed")
    return "Server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
