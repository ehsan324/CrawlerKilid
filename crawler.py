import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

API_URL = 'http://127.0.0.1:8000/api/listings/'
BASE_URL = 'https://kilid.com'
start_page = 1
end_page = 5


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def extract_info(session, href):
    info = {
        'name': '',
        'image_url': '',
        'price': '',
        'facilities': '',
        'address': '',
    }
    html = await fetch(session, href)
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('div', class_='h-[115px] flex flex-col justify-between')
    info['name'] = name.find('p', class_='font-bold').text.strip() if name else 'N/A'

    img = soup.find('img', class_='w-full property-picture')
    if img:
        info['image_url'] = img.get('alt')
    else:
        print(f"No image found for URL: {href}")

    facilities = soup.find('div', class_='justify-start w-full space-y-6 align-middle felx md:columns-3 columns-2')
    if facilities:
        facility_list = [facility.text.strip() for facility in facilities.find_all('div', class_='flex flex-row justify-start align-middle')]
        info['facilities'] = ', '.join(facility_list)

    price = soup.find('h1', class_='mb-6 font-semiBold text-primary-800 text-display-sm')
    info['price'] = price.text.strip() if price else 'N/A'

    address = soup.find('p', class_='inline-flex mb-6')
    info['address'] = address.text.strip() if address else 'N/A'

    return info


async def save_to_api(session, data):
    
    async with session.post(API_URL, json=data) as response:
        if response.status == 201:
            print("Data saved successfully.")
        else:
            print(f"Failed to save data: {response.status}")




async def extract_links(session, url):
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', class_='style_plp-card-link__yPlrt')
    return [BASE_URL + link['href'] for link in links]


async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_num in range(start_page, end_page + 1):
            url = f'{BASE_URL}/buy/tehran?listingTypeId=1&location=272905&page={page_num}'
            print(f'Extracting page {page_num}')
            links = await extract_links(session, url)
            for link in links:
                info = await extract_info(session, link)
                tasks.append(save_to_api(session, info)) 
                

        await asyncio.gather(*tasks)  

    end = time.time()
    print(f"Total time taken: {end - start} seconds")

if __name__ == "__main__":
    asyncio.run(main())
