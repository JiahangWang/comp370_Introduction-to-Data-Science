import argparse
import json
import requests
import os
from bs4 import BeautifulSoup

cookies = {
    'political-ad-opt-out': '{"data":false,"exp":604800000,"ts":1698156005533,"mac":-548428023}',
    'permutive-id': 'f2083472-c4e5-411f-a2ab-405ec6fc3497',
    '_pctx': '%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBmATgHYATIL4AOfgAYJAVgAs3QR1EgAvkA',
    '_pcid': '%7B%22browserId%22%3A%22lo4e8oa0am9g4gp0%22%7D',
    '_pcus': 'eyJ1c2VyU2VnbWVudHMiOm51bGx9',
    '_gcl_au': '1.1.502445051.1698156006',
    '_vfa': 'montrealgazette%2Ecom.00000000-0000-4000-8000-0580b1fbbf89.e03234ef-dad5-4038-98bf-e70f81ef51c8.1698156006.1698156006.1698156006.1',
    '__pat': '-14400000',
    '_parsely_session': '{%22sid%22:1%2C%22surl%22:%22https://montrealgazette.com/category/news/%22%2C%22sref%22:%22%22%2C%22sts%22:1698156006349%2C%22slts%22:0}',
    '_parsely_visitor': '{%22id%22:%22pid=012b68bc-3892-44c8-93ed-082babfa41fc%22%2C%22session_count%22:1%2C%22last_session_ts%22:1698156006349}',
    '_gid': 'GA1.2.1402322302.1698156006',
    '___nrbi': '%7B%22firstVisit%22%3A1698156006%2C%22userId%22%3A%229b6b922c-3aa3-4122-aec2-543f1330dc83%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1698156006%2C%22timesVisited%22%3A1%7D',
    'compass_uid': '9b6b922c-3aa3-4122-aec2-543f1330dc83',
    'cX_G': 'cx%3A2pahvq7pxtbds3b1864k7usy9i%3A31axunenrs9v6',
    'sailthru_pageviews': '3',
    'sailthru_content': 'd07be313b2d77576a1255d994cf0573cbb570a35e5eb0c0930dce6e290ed0507',
    'sailthru_visitor': '2e543bf1-6798-42ac-abb4-2ed92a8a209d',
    '__pvi': 'eyJpZCI6InYtbG80ZThvYTZta2VrNHo5eCIsImRvbWFpbiI6Ii5tb250cmVhbGdhemV0dGUuY29tIiwidGltZSI6MTY5ODE1NjAyNzMxNH0%3D',
    'x-id': '{"data":{"adLight":false,"id":"neubaf8wjnlw1a811gub5yclb6cpu9cvkxnolc3znp","updated":1698156027384,"printSubscriber":false},"exp":604800000,"ts":1698156027384,"mac":1541271168}',
    'mprtcl-v4_4662F03F': "{'gs':{'ie':1|'dt':'us1-99b65fde89a1a145894d2d51d283cc83'|'av':'1.0.0'|'cgid':'aadd78f0-aa18-4492-b310-354eb524dd1b'|'das':'eca34c2d-2a9e-4c19-cf12-fc90698a1e3e'|'csm':'WyItMjkwMjAxNTAyMTE3NjQ0MjUyOSJd'|'sid':'2F741E6B-60B6-4660-3E6D-5200735A2708'|'les':1698156027442|'ssd':1698156006000}|'l':1|'-2902015021176442529':{'fst':1698156006167|'ui':'eyIwIjoibmV1YmFmOHdqbmx3MWE4MTFndWI1eWNsYjZjcHU5Y3ZreG5vbGMzem5wIn0='}|'cu':'-2902015021176442529'}",
    '__tbc': '%7Bkpex%7DWanIZJ8mDdaOB65QQmdaoIpBAqBMEyOHCnpo3byKgFOtYospKvtLvFqS4qS-ZcC5',
    'xbc': '%7Bkpex%7D65i4b9j1NrxcI4s90PNFKlp3NdeeK3viUFnGFWtqUXBSvPgPEjEyuoYn4OLr7SeZj6G4CiQC7SLxOtN2MIyveKCKIWUEW-zky-zM_NaW0Fo',
    'cX_P': 'lo4e8oa0am9g4gp0',
    '_ga_72QH41ZTMR': 'GS1.1.1698156006.1.1.1698156027.39.0.0',
    '_vfb': 'montrealgazette%2Ecom.00000000-0000-4000-8000-0580b1fbbf89.6..1698156006.true...',
    '___nrbic': '%7B%22previousVisit%22%3A1698156006%2C%22currentVisitStarted%22%3A1698156006%2C%22sessionId%22%3A%229a1c738a-fe40-4c48-95cc-35a2ca9b2706%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A3%2C%22landingPage%22%3A%22https%3A//montrealgazette.com/category/news/%22%2C%22referrer%22%3A%22%22%7D',
    '_ga_9H6VPHFHKG': 'GS1.1.1698156006.1.1.1698156027.39.0.0',
    '_ga_P2D16LEV65': 'GS1.2.1698156006.1.1.1698156027.0.0.0',
    '_ga': 'GA1.2.388968270.1698156006',
}

headers = {
    'authority': 'montrealgazette.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'political-ad-opt-out={"data":false,"exp":604800000,"ts":1698156005533,"mac":-548428023}; permutive-id=f2083472-c4e5-411f-a2ab-405ec6fc3497; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBmATgHYATIL4AOfgAYJAVgAs3QR1EgAvkA; _pcid=%7B%22browserId%22%3A%22lo4e8oa0am9g4gp0%22%7D; _pcus=eyJ1c2VyU2VnbWVudHMiOm51bGx9; _gcl_au=1.1.502445051.1698156006; _vfa=montrealgazette%2Ecom.00000000-0000-4000-8000-0580b1fbbf89.e03234ef-dad5-4038-98bf-e70f81ef51c8.1698156006.1698156006.1698156006.1; __pat=-14400000; _parsely_session={%22sid%22:1%2C%22surl%22:%22https://montrealgazette.com/category/news/%22%2C%22sref%22:%22%22%2C%22sts%22:1698156006349%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22pid=012b68bc-3892-44c8-93ed-082babfa41fc%22%2C%22session_count%22:1%2C%22last_session_ts%22:1698156006349}; _gid=GA1.2.1402322302.1698156006; ___nrbi=%7B%22firstVisit%22%3A1698156006%2C%22userId%22%3A%229b6b922c-3aa3-4122-aec2-543f1330dc83%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1698156006%2C%22timesVisited%22%3A1%7D; compass_uid=9b6b922c-3aa3-4122-aec2-543f1330dc83; cX_G=cx%3A2pahvq7pxtbds3b1864k7usy9i%3A31axunenrs9v6; sailthru_pageviews=3; sailthru_content=d07be313b2d77576a1255d994cf0573cbb570a35e5eb0c0930dce6e290ed0507; sailthru_visitor=2e543bf1-6798-42ac-abb4-2ed92a8a209d; __pvi=eyJpZCI6InYtbG80ZThvYTZta2VrNHo5eCIsImRvbWFpbiI6Ii5tb250cmVhbGdhemV0dGUuY29tIiwidGltZSI6MTY5ODE1NjAyNzMxNH0%3D; x-id={"data":{"adLight":false,"id":"neubaf8wjnlw1a811gub5yclb6cpu9cvkxnolc3znp","updated":1698156027384,"printSubscriber":false},"exp":604800000,"ts":1698156027384,"mac":1541271168}; mprtcl-v4_4662F03F={\'gs\':{\'ie\':1|\'dt\':\'us1-99b65fde89a1a145894d2d51d283cc83\'|\'av\':\'1.0.0\'|\'cgid\':\'aadd78f0-aa18-4492-b310-354eb524dd1b\'|\'das\':\'eca34c2d-2a9e-4c19-cf12-fc90698a1e3e\'|\'csm\':\'WyItMjkwMjAxNTAyMTE3NjQ0MjUyOSJd\'|\'sid\':\'2F741E6B-60B6-4660-3E6D-5200735A2708\'|\'les\':1698156027442|\'ssd\':1698156006000}|\'l\':1|\'-2902015021176442529\':{\'fst\':1698156006167|\'ui\':\'eyIwIjoibmV1YmFmOHdqbmx3MWE4MTFndWI1eWNsYjZjcHU5Y3ZreG5vbGMzem5wIn0=\'}|\'cu\':\'-2902015021176442529\'}; __tbc=%7Bkpex%7DWanIZJ8mDdaOB65QQmdaoIpBAqBMEyOHCnpo3byKgFOtYospKvtLvFqS4qS-ZcC5; xbc=%7Bkpex%7D65i4b9j1NrxcI4s90PNFKlp3NdeeK3viUFnGFWtqUXBSvPgPEjEyuoYn4OLr7SeZj6G4CiQC7SLxOtN2MIyveKCKIWUEW-zky-zM_NaW0Fo; cX_P=lo4e8oa0am9g4gp0; _ga_72QH41ZTMR=GS1.1.1698156006.1.1.1698156027.39.0.0; _vfb=montrealgazette%2Ecom.00000000-0000-4000-8000-0580b1fbbf89.6..1698156006.true...; ___nrbic=%7B%22previousVisit%22%3A1698156006%2C%22currentVisitStarted%22%3A1698156006%2C%22sessionId%22%3A%229a1c738a-fe40-4c48-95cc-35a2ca9b2706%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A3%2C%22landingPage%22%3A%22https%3A//montrealgazette.com/category/news/%22%2C%22referrer%22%3A%22%22%7D; _ga_9H6VPHFHKG=GS1.1.1698156006.1.1.1698156027.39.0.0; _ga_P2D16LEV65=GS1.2.1698156006.1.1.1698156027.0.0.0; _ga=GA1.2.388968270.1698156006',
    'if-modified-since': 'Tue, 24 Oct 2023 13:57:29 GMT',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

filename = 'homepage.html'

url = 'https://montrealgazette.com/category/news/'


def get_homepage():
    # Check if the file already exists
    if os.path.isfile(filename):
        # The file exists, read from the file
        print(f"Reading data from {filename}...")
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        # The file does not exist, fetch data from the web
        print(f"Fetching data from {url}...")
        try:
            response = requests.get(url, cookies=cookies, headers=headers)
            response.raise_for_status()  # Check if the request was successful
            content = response.text

            # Write the fetched content to a file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
        except requests.HTTPError as http_err:
            print(f"HTTP error: {http_err}")  # Handle HTTP errors
        except Exception as err:
            print(f"Other error occurred: {err}")  # Handle other potential errors
        else:
            print("Content successfully saved to file.")

    return content


def get_Trending_urls(content):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')

    # Find all <a> tags with a specific class
    a_tags = soup.find_all('a', class_='article-card__link')

    # Select the first 5 <a> tags and get their 'href' attributes, appending the base URL
    base_url = 'https://montrealgazette.com'
    urls = []
    for a_tag in a_tags[:5]:  # Limiting to the first 5
        href = a_tag.get('href')
        if href:  # Making sure 'href' is present
            # Check if href is already a complete URL
            full_url = href if href.startswith('http') else base_url + href
            urls.append(full_url)

    return urls


def get_trendings(urls):
    contents = []  # List to store the content of web pages
    directory = "Trendings"  # Set the directory name to store the content

    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, url in enumerate(urls, start=1):
        filepath = os.path.join(directory, f'trending_{i}.html')

        if os.path.isfile(filepath):
            # If the file exists, read content from the file
            print(f"Reading data from {filepath}...")
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            # If the file does not exist, fetch content from the web
            print(f"Fetching data from {url}...")
            try:
                response = requests.get(url, cookies=cookies, headers=headers)
                response.raise_for_status()  # Check if the request was successful
                content = response.text

                # Write the fetched content to a file
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
            except requests.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
                content = ''  # Use an empty string in case of errors
            except Exception as err:
                print(f"An error occurred: {err}")  # Handle other errors
                content = ''  # Use an empty string in case of errors

        # Add the content to the list
        contents.append(content)

    return contents


def collect_trendings(contents, outputFileName):
    # List to store all the articles' information
    articles_info = []

    for content in contents:
        soup = BeautifulSoup(content, 'html.parser')

        # Extracting the required information
        title_tag = soup.find('h1', id='articleTitle')
        date_tag = soup.find('span', class_='published-date__since')
        author_parent_tag = soup.find('span', class_='published-by__author')
        author_tag = author_parent_tag.find('a') if author_parent_tag else None
        blurb_tag = soup.find('p', class_='article-subtitle')

        # Getting the text if the respective tags are found, else use an empty string
        title = title_tag.get_text() if title_tag else ""
        publication_date = date_tag.get_text() if date_tag else ""
        author = author_tag.get_text() if author_tag else ""
        blurb = blurb_tag.get_text() if blurb_tag else ""

        # Adding to the list of article information
        article_info = {
            "title": title.strip(),
            "publication_date": publication_date.strip(),
            "author": author.strip(),
            "blurb": blurb.strip()
        }
        articles_info.append(article_info)

    # Writing the information into a JSON file
    with open(outputFileName, 'w', encoding='utf-8') as outfile:
        json.dump(articles_info, outfile, ensure_ascii=False, indent=4)


def main():
    content = get_homepage()
    urls = get_Trending_urls(content)
    contents = get_trendings(urls)
    collect_trendings(contents, outputFileName)



if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Collect trending article information.')

    # Add the arguments
    parser.add_argument('-o', '--output', required=True, help='The JSON output file name', type=str)

    # Parse the arguments
    args = parser.parse_args()

    # The output file name is retrieved from the arguments
    outputFileName = args.output

    main()
