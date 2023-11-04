from flask import Flask,request,jsonify
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
app = Flask(__name__)
CORS(app)
all_result=[]
class Webscrapper:
    
    @app.route('/website-info',methods=['POST'])
    def website_info(): 
        data=request.get_json()
        url=data.get('title')
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            word_count = len(soup.get_text().split())
            web_links = [a['href'] for a in soup.find_all('a', href=True)]
            media_links = [img['src'] for img in soup.find_all('img', src=True)]
            result = {
                "domain": url,
                "word_count": word_count,
                "web_links": web_links,
                "media_links": media_links,
                "favourite": "false"
            }
            all_result.insert(0, result)
            return all_result
        else:
            return {"error":"unable to process the request right now"}


    @app.route('/settodefault', methods=['GET'])
    def setdefault():
        global all_result
        all_result=[]
        return {"msg":"default is working fine"}
    
    @app.route('/delete/<int:index>', methods=['DELETE'])
    def deleteitem(index):
        if index < 0 or index >= len(all_result):
            return jsonify({"error": "Invalid index"}), 400

        deleted_item = all_result.pop(index)
        return all_result,200
    
    @app.route('/updatefav/<int:index>', methods=['PUT'])
    def updateitem(index):
        if index < 0 or index >= len(all_result):
            return jsonify({"error": "Invalid index"}), 400
        all_result[index]["favourite"] = "true" if all_result[index]["favourite"] == "false" else "false"
        return all_result,200


if __name__ == '__main__':
    app.run(debug=True)
