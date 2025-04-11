from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your ScraperAPI key
SCRAPER_API_KEY = '1981e43459b56dd9d4b35b81c251a8a5'

def fetch_cases():
    cases = []

    # EU cases
    try:
        eu_url = f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://competition-policy.ec.europa.eu/mergers/publications_en'
        eu_response = requests.get(eu_url)
        eu_soup = BeautifulSoup(eu_response.text, 'html.parser')
        for row in eu_soup.select('.view-merger-publications tbody tr')[:5]:
            columns = row.find_all('td')
            if columns:
                case_name = columns[0].get_text(strip=True)
                date = columns[2].get_text(strip=True)
                link = 'https://competition-policy.ec.europa.eu' + columns[0].find('a')['href']
                cases.append({
                    'caseName': case_name,
                    'jurisdiction': 'EU',
                    'status': 'N/A',
                    'date': date,
                    'link': link
                })
    except Exception as e:
        print(f'EU Fetch Error: {e}')

    # UK cases
    try:
        uk_url = f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.gov.uk/cma-cases'
        uk_response = requests.get(uk_url)
        uk_soup = BeautifulSoup(uk_response.text, 'html.parser')
        for row in uk_soup.select('.gem-c-document-list__item')[:5]:
            title = row.select_one('.gem-c-document-list__item-title').get_text(strip=True)
            link = 'https://www.gov.uk' + row.find('a')['href']
            date = row.select_one('.gem-c-document-list__attribute')
            date_text = date.get_text(strip=True) if date else 'N/A'
            cases.append({
                'caseName': title,
                'jurisdiction': 'UK',
                'status': 'N/A',
                'date': date_text,
                'link': link
            })
    except Exception as e:
        print(f'UK Fetch Error: {e}')

    # Australia cases
    try:
        au_url = f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.accc.gov.au/public-registers/mergers-registers/public-informal-merger-reviews'
        au_response = requests.get(au_url)
        au_soup = BeautifulSoup(au_response.text, 'html.parser')
        for row in au_soup.select('.view-mergers-public-register .views-row')[:5]:
            title = row.select_one('.field-content a').get_text(strip=True)
            link = 'https://www.accc.gov.au' + row.select_one('.field-content a')['href']
            cases.append({
                'caseName': title,
                'jurisdiction': 'Australia',
                'status': 'N/A',
                'date': 'N/A',
                'link': link
            })
    except Exception as e:
        print(f'Australia Fetch Error: {e}')

    return cases

@app.get("/mergers")
def get_merger_cases():
    return fetch_cases()