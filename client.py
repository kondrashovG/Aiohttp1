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
#     "http://127.0.0.1:5000/ad/2", json={'description': 'Отдам рыбку в добрые руки'}
# )
response = requests.get(
    "http://127.0.0.1:5000/ad/10",
)
# response = requests.delete(
#     "http://127.0.0.1:5000/ad/2",
# )
print(response.json())
