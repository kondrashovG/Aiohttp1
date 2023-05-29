import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        # response = await session.post(
        #     "http://127.0.0.1:8080/ad/",
        #     json={"title": "Объявление 1", "description": "Отдам котят в добрые руки", "owner": "Дядя Фёдор"})
        # print(response)
        # json_data = await response.json()
        # print(json_data)
        # response = await session.post(
        #     "http://127.0.0.1:5000/ad/",
        #     json={"title": "Объявление 2", "description": "Отдам щенков в добрые руки", "owner": "Шарик"})
        # json_data = await response.json()
        # print(json_data)
        # response = await session.post(
        #     "http://127.0.0.1:5000/ad/",
        #     json={"title": "Объявление 3", "description": "Куплю корову", "owner": "Кот Матроскин"})
        # json_data = await response.json()
        # print(json_data)
        # response = await session.post(
        #     "http://127.0.0.1:5000/ad/",
        #     json={"title": "Объявление 4", "description": "Ищу друзей", "owner": "Крокодил Гена"})
        # json_data = await response.json()
        # print(json_data)
        # response = await session.post(
        #     "http://127.0.0.1:5000/ad/",
        #     json={"title": "Объявление 5", "description": "Приму апельсины в дар", "owner": "Чебурашка"})
        # json_data = await response.json()
        # print(json_data)
        #
        #
        async with session.get("http://127.0.0.1:8080/ad/21") as resp:
            print(resp)
            response = await resp.read()
            print(response)
        # print(json_data)
        # response = await session.get("http://127.0.0.1:5000/ad/22")
        # json_data = await response.json()
        # print(json_data)
        # response = await session.get("http://127.0.0.1:5000/ad/23")
        # json_data = await response.json()
        # print(json_data)
        # response = await session.get("http://127.0.0.1:5000/ad/24")
        # json_data = await response.json()
        # print(json_data)
        # response = await session.get("http://127.0.0.1:5000/ad/25")
        # json_data = await response.json()
        # print(json_data)

        # response = await session.patch(
        #     "http://127.0.0.1:5000/ad/5", json={'description': 'Отдам рыбку в добрые руки'}
        # )
        # json_data = await response.json()

        # response = await session.delete("http://127.0.0.1:5000/ad/21")
        # json_data = await response.json()
        # response = await session.delete("http://127.0.0.1:5000/ad/22")
        # json_data = await response.json()
        # response = await session.delete("http://127.0.0.1:5000/ad/23")
        # json_data = await response.json()
        # response = await session.delete("http://127.0.0.1:5000/ad/24")
        # json_data = await response.json()
        # response = await session.delete("http://127.0.0.1:5000/ad/25")
        # json_data = await response.json()
        # print(json_data)

        # response = requests.patch(
        #     "http://127.0.0.1:5000/ad/1", json={'description': 'Отдам рыбку в добрые руки'}
        # )



asyncio.run(main())
