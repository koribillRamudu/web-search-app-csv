from flask import Flask, request, jsonify
import csv
from threading import Thread
from webcrawler import WebCrawler
from indexer import Indexer
from ranker import Ranker

app = Flask(__name__)
crawler = None

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the search API."

@app.route('/api/search', methods=['GET'])
def search():
    global crawler
    keyword = request.args.get('keyword')
    url = request.args.get('url')
    if keyword and url:
        if crawler is None:
            crawler = WebCrawler()
        # Threading for crawling
        crawler_thread = Thread(target=crawler.crawl, args=(url,))
        crawler_thread.start()
        
        # Wait for the crawling to finish and then index documents
        crawler_thread.join()
        results = index_documents(keyword)

        if results:
            return jsonify(results)
        else:
            return jsonify({'message': 'Result not found for the given keyword and URL.'}), 404
    else:
        return jsonify({'error': 'Both keyword and URL parameters are required.'}), 400

def index_documents(keyword):
    indexer = Indexer()
    indexer.index = crawler.index
    results = indexer.search(keyword)
    if results:
        ranker = Ranker()
        ranked_results = ranker.rank_results(results, indexer.index, keyword)
        return ranked_results
    else:
        return None

@app.route('/api/csvdata', methods=['GET'])
def csv_data():
    data = []
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return jsonify(data)

@app.route('/api/csvdata', methods=['POST'])
def add_data():
    # Parse JSON data from the request
    new_data = request.json.get('name')
    new_data1= request.json.get('age')
    new_data2= request.json.get('city')

    if new_data:
        # Append new data to the CSV file
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_data,new_data1,new_data2])

        return jsonify({'message': 'Data added successfully.'}), 201
    else:
        return jsonify({'error': 'Data field is missing from the request.'}), 400

if __name__ == '__main__':
    app.run(debug=True)