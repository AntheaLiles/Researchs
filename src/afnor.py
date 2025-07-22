import requests, csv, time
from bs4 import BeautifulSoup

base_url = "https://norminfo.afnor.org/search?typeResult=normes-publiees&cosID=348&domainID=11581"
headers = {"User-Agent": "Mozilla/5.0"}

def safe_select_text(soup, selector):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else ""

def get_page_url(page_num):
    # The site uses ?page= for pagination
    return f"{base_url}&page={page_num}"

with open('normes_construction.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Reference','Titre','Date_pub','Pages','Codes_ICS','Indice_classement'])
    page_num = 1
    total_scraped = 0
    while True:
        print(f"Scraping page {page_num}...")
        res = requests.get(get_page_url(page_num), headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('tbody tr')
        if not rows:
            print("No more rows found, stopping.")
            break
        for row in rows:
            try:
                ref = safe_select_text(row, 'td:nth-of-type(2)')
                titre = safe_select_text(row, 'td:nth-of-type(1)')
                if not ref:
                    continue
                search_url = f"https://www.boutique.afnor.org/fr-fr/resultats?Keywords={ref.replace(' ','%20')}&StandardStateIds=1"
                res2 = requests.get(search_url, headers=headers)
                soup2 = BeautifulSoup(res2.text, 'html.parser')
                link = soup2.select_one('.products div.product-title a')
                if not link:
                    continue
                norme_url = "https://www.boutique.afnor.org" + link['href']
                res3 = requests.get(norme_url, headers=headers)
                soup3 = BeautifulSoup(res3.text, 'html.parser')
                date_pub = safe_select_text(soup3, '#label-control-date-parution + .value')
                pages = safe_select_text(soup3, '#label-control-nb-pages + .value')
                ics_list = [item.get_text(strip=True) for item in soup3.select('#label-control-codesICS + .value li')]
                ics = ", ".join(ics_list)
                indice = safe_select_text(soup3, '#label-control-indice + .value')
                writer.writerow([ref, titre, date_pub, pages, ics, indice])
                total_scraped += 1
                time.sleep(1)  # Be polite to the server
            except Exception as e:
                print(f"Error processing {ref}: {e}")
        page_num += 1
    print(f"Total entries scraped: {total_scraped}")