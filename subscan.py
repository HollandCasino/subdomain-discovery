import asyncio
import httpx
from bs4 import BeautifulSoup

def fetch_html_content(url):
    response = httpx.get(url)
    return response.text

def find_matching_domains(td_texts, domain):
    printed_strings = set()
    for td_text in td_texts:
        if domain in td_text.lower() and td_text.count('.') == 2 and td_text not in printed_strings:
            printed_strings.add(td_text)
    return printed_strings

def prepare_urls(printed_strings):
    urls = ["http://" + td_text for td_text in printed_strings] + ["https://" + td_text for td_text in printed_strings]
    return urls

async def check_status_code(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=1)
            return url, response.status_code
        except httpx.RequestError:
            return url, -1

async def check_status_codes(urls):
    tasks = [check_status_code(url) for url in urls]
    return await asyncio.gather(*tasks)

def print_sorted_status_codes(status_codes):
    status_codes.sort(key=lambda x: x[1])
    for sc_check, status_code in status_codes:
        print(f"{sc_check}: {status_code}")

def main():
    domain = input("What is the domain? Example: google.nl  :   ")
    url = "https://crt.sh/?q=" + domain

    response = fetch_html_content(url)
    soup = BeautifulSoup(response, "html.parser")
    td_texts = [td.get_text() for td in soup.find_all("td")]

    printed_strings = find_matching_domains(td_texts, domain)
    urls = prepare_urls(printed_strings)

    # Asynchronously check status codes
    status_codes = asyncio.run(check_status_codes(urls))
    print_sorted_status_codes(status_codes)

if __name__ == "__main__":
    main()
