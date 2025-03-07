import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Function to search GitHub repositories
def search_github(topic):
    url = f"https://api.github.com/search/repositories?q={topic}&per_page=100"
    headers = {
        'Authorization': 'Bearer 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'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        repositories = []
        for item in results['items']:
            repositories.append({
                'name': item['name'],
                'url': item['html_url'],
                'description': item['description'],
                'download_url': f"https://github.com/{item['full_name']}/archive/refs/heads/main.zip"
            })
        return repositories
    else:
        return []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    topic = request.args.get('topic')
    if topic:
        repositories = search_github(topic)
        return render_template('index.html', topic=topic, results=repositories)
    else:
        return jsonify({"error": "No topic provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
