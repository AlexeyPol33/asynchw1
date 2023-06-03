from model import engine, Session, SwapiPeople,get_model_keys
from more_itertools import chunked


import asyncio
import aiohttp

URL = 'https://swapi.dev/api/people/'

async def post(jsons):
    
    async with Session() as session:
        
        for json in jsons:
            keys = await get_model_keys()
            filtered_dict = {key: value for key, value in json.items() if key in keys}
            swapiPeople = SwapiPeople(**filtered_dict)
            session.add(swapiPeople)
        await session.commit()

async def request(id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'{URL}{id}/')
        data = await response.json()
        data['id'] = id
        return data
    
async def main():

    request_tasks = []
    for i in range(1,84):
        request_tasks.append(asyncio.create_task(request(i)))
    
    request_tasks_chunked = chunked(request_tasks,5)

    posts_tasks = []
    for tasks_chunk in request_tasks_chunked:
        req = await asyncio.gather(*tasks_chunk)
        posts_tasks.append(asyncio.create_task(post(req)))

    await asyncio.gather(*posts_tasks)
   
       
    
     

if __name__ == '__main__':
    asyncio.run(main())
    print ('Загрузка завершена')