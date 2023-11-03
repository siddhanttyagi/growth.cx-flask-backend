from flask import Flask,request,jsonify
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
app = Flask(__name__)
CORS(app)
all_result=[]
class Webscrapper:
    
    @app.route('/member',methods=['POST'])
    def hello_world(): 
        data=request.get_json()
        url=data.get('title')
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            word_count = len(soup.get_text().split())
            web_links = [a['href'] for a in soup.find_all('a', href=True)]
            media_links = [img['src'] for img in soup.find_all('img', src=True)]
            result = {
                "word_count": word_count,
                "web_links": web_links,
                "media_links": media_links
            }
            all_result.append(result)
            return all_result
        else:
            return {"kop":"alpha"}



if __name__ == '__main__':
    app.run(debug=False)
