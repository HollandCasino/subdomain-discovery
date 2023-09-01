import requests
from bs4 import BeautifulSoup
import httpx
import asyncio
import time

def fetch_html_content(url):
    response = requests.get(url)
    return response.text

def find_matching_domains(td_texts, domain):
    printed_strings = set()
    for td_text in td_texts:
        if domain in td_text.lower() and td_text.count('.') == 2 and td_text not in printed_strings:
            printed_strings.add(td_text)
    return printed_strings

def prepare_urls(printed_strings):

    urls = set()
    for x in printed_strings:
        urls.add("http://" + x)
        urls.add("https://" + x)
    return urls

async def sc_check(urls):

    check_urls = list(urls)
    start_time = time.time()

    for x in check_urls:
        try:
            async with httpx.AsyncClient(verify=True, timeout=5.0) as client:
                check = await client.get(x)
                print(f"{x}: {check.status_code}") 
                
        except httpx.RequestError as e:
            print(f"{x}: Error - {e}")

    print("\n", "Process finished --- %s seconds ---" % (time.time() - start_time))

    return x, check.status_code

def main():
    
    domain = input("What is the domain? Example: google.nl: ")
    url = "https://crt.sh/?q=" + domain

    try:
        response = fetch_html_content(url)
        soup = BeautifulSoup(response, "html.parser")
        td_texts = [td.get_text() for td in soup.find_all("td")]
        printed_strings = find_matching_domains(td_texts, domain)
        urls = prepare_urls(printed_strings)
        asyncio.run(sc_check(urls))

    except requests.RequestException as e:
        print("Error fetching or parsing data:", e)
    except KeyboardInterrupt:
        print("Operation interrupted by user.")


if __name__ == "__main__":
    main()
