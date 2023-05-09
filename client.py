import requests

# response = requests.post(
#     "http://127.0.0.1:5000/ad/",
#     json={
#         "title": "Объявление 2",
#         "description": "Отдам котят в добрые руки",
#         "owner": "Дядя Фёдор",
#     },
# )
# response = requests.patch(
#     "http://127.0.0.1:5000/ad/9", json={'description': 'Отдам щенков в добрые руки'}
# )
response = requests.get(
    "http://127.0.0.1:5000/ad/1",
)
# response = requests.delete(
#     "http://127.0.0.1:5000/ad/1",
# )
print(response.json())
