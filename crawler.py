import asyncio
from aiohttp import ClientSession
from codetiming import Timer


def get_url_paginated(max_url: int) -> list:
    url_list = [f'https://rickandmortyapi.com/api/character/?page={n}' for n in range(max_url) if not n > 42]
    return url_list


async def get_details(resp):
    results = resp['results']
    for n in range(len(results)):
        name = results[n]['name']
        status = results[n]['status']
        species = results[n]['species']
        data = {
            'name': name,
            'status': status,
            'species': species
        }
        return data


async def task(name, work_queue):
    """
     task() as an asynchronous function.
    :param name: Task name
    :param work_queue:
    :return:
    """
    timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    async with ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f"Task {name} getting URL: {url}")
            timer.start()
            async with session.get(url) as response:
                resp = await response.json()
            timer.stop()


async def main():
    """
    This is the main entry point for the program
    """
    work_queue = asyncio.Queue()
    url_list = get_url_paginated(50)
    print(url_list)
    for url in url_list:
        await work_queue.put(url)
    # Run the task
    with Timer(text="\nTotal elapsed time: {:.1f}"):
        await asyncio.gather(
            asyncio.create_task(task("One", work_queue)),
            asyncio.create_task(task("Two", work_queue)),
        )


def crawler():
    return asyncio.run(main())
