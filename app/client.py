import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:


        async with session.post(
            "http://127.0.0.1:8080/user",
            json={"name": "test",
                  "password": "testtest"},
            headers={
                "Content-Type": "application/json",
                "token": "xxxxxxx"}
        ) as response:
            print(response.status)
            print(await response.json())

        # async with session.get(
        #     "http://127.0.0.1:8080/user/1"
        # ) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.patch(
        #     "http://127.0.0.1:8080/user/1",
        #     json={'name': 'test2',
        #           'password': 'testtesttest'}
        # ) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.delete(
        #     "http://127.0.0.1:8080/user/1"
        # ) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.post(
        #     "http://127.0.0.1:8080/advertisement",
        #     json={'title': 'test',
        #           'description': 'testtest',
        #           'owner_id': 1}
        # ) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.get(
        #     "http://127.0.0.1:8080/advertisement/1"
        # ) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.patch(
        #     "http://127.0.0.1:8080/advertisement/1",
        #     json={'title': 'test2',
        #           'description': 'testtesttest'}
        # ) as response:
        #     print(response.status)
        #     print(await response.json())

        # async with session.delete(
        #     "http://127.0.0.1:8080/advertisement/1"
        # ) as response:
        #     print(response.status)
        #     print(await response.json())
        #

asyncio.run(main())
