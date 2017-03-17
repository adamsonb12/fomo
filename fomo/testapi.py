import requests

data = requests.get('http://127.0.0.1:8000/api/products/?min_price=1&max_price=500')
print(data.json())