import requests,json 
import ast

r = requests.get('http://127.0.0.1:8000/posts/user/4')
jsonic = json.loads(r.text)


    


