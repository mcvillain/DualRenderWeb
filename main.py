from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

def fetch_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except requests.RequestException as e:
        return f"Error fetching content: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    url1 = request.form.get('url1')
    url2 = request.form.get('url2')
    
    if not url1 or not url2:
        return jsonify({'error': 'Both URLs are required'}), 400
    
    if not urlparse(url1).scheme:
        url1 = 'http://' + url1
    if not urlparse(url2).scheme:
        url2 = 'http://' + url2
    
    content1 = fetch_content(url1)
    content2 = fetch_content(url2)
    
    return jsonify({
        'content1': content1,
        'content2': content2
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
