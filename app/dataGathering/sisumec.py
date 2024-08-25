from sqlalchemy.orm import Session
from db import models, schema
import requests, json, asyncio, time, aiohttp

async def save_data(data):
    with open('data.json', 'a') as outfile:
        json_str = json.dumps(data)
        outfile.write(json_str + '\n')

#THIS METHOD CAUSES 504 ERRORS AFTER A WHILE, IT'S TOO MUCH FOR THE API TO HANDLE
# async def get_selected_enem(course):
#         async with aiohttp.ClientSession() as session2:
#             async with session2.get(f"https://sisu-api.sisu.mec.gov.br/api/v1/oferta/{course}/selecionados") as response2:
#                 try:
#                     selected = await response2.json()
#                     return selected
#                 except:
#                     print(course)

#COMMENTED SECTIONS ARE FOR USE WITH THE ABOVE FUNCTION, NOW IT USES A FOR LOOP WITH REQUESTS METHOD, WICH IS WAY WAY SLOWER,
#BUT IN GOES EASIER ON THE API AND ACTUALLY GETS MOST OF THE DATA, THERE'S STILL SOME ERRORS THOUGH
async def get_stuff_from_sisu(site):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://sisu-api.sisu.mec.gov.br/api/v1/oferta/instituicao/{site['co_ies']}") as response:
                data = await response.json()
                del data['search_rule']
                #tasks2 = []
                for j in data:
                    del data[j]['ds_documentacao']
                    selected  = requests.get(f"https://sisu-api.sisu.mec.gov.br/api/v1/oferta/{data[j]['co_oferta']}/selecionados").json()
                    data[j]['selecionados'] = selected
                #    new_task_2 = asyncio.create_task(get_selected_enem(data[j]['co_oferta']))
                #    tasks2 += [new_task_2]
                # selected = await asyncio.gather(*tasks2)
                # for k in data:
                #     data[k]['selecionados'] = selected
                site['data'] = data
                await save_data(site)
    except Exception as e:
        print(site)
        print(e)

async def main():
    print(f"Starting scrapping of SISU/MEC data at {time.strftime('%X')}...")
    tasks = []
    institutions = requests.get("https://sisu-api.sisu.mec.gov.br/api/v1/oferta/instituicoes").json()
    for i in institutions:
        new_task = asyncio.create_task(get_stuff_from_sisu(i))
        tasks.append(new_task)

    await asyncio.gather(*tasks)
    print(f"Done scrapping SISU/MEC data at {time.strftime('%X')}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())



