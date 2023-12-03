import asyncio
import aiohttp
from pprint import pprint

from sqlalchemy.exc import IntegrityError

from tools import to_string
from models import init_db, Session, Swapi
import datetime


async def get_person(person_id):
    session = aiohttp.ClientSession()
    response = await session.get(f'https://swapi.dev/api/people/{person_id}/')
    info = await response.json()
    films = to_string('films', info, session)
    species = to_string('species', info, session)
    starships = to_string('starships', info, session)
    vehicles = to_string('vehicles', info, session)
    result = await asyncio.gather(films, species, vehicles, starships)
    info.pop('created')
    info.pop('edited')
    info['id'] = person_id
    await session.close()
    return info


async def work_with_db(person_dict):
    try:
        async with Session() as session:
            person = Swapi(person_id=person_dict['id'], json=person_dict)
            session.add(person)
            await session.commit()
            return {'status': 'ok'}
    except IntegrityError as error:
        raise ValueError('Такой персонаж уже есть!')


async def main():
    start = datetime.datetime.now()
    await init_db()
    info = await get_person(2)
    await work_with_db(info)
    # work_with_db_task = asyncio.create_task(work_with_db(info))
    finish = datetime.datetime.now()
    time = finish - start
    print(time)

asyncio.run(main())