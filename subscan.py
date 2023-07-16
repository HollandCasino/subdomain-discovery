import requests
from bs4 import BeautifulSoup
import httpx

# https://github.com/HollandCasino
# This script uses https://crt.sh/ to uncover both active and expired subdomains.
# The status_code "-1" represent an error. 

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
    urls = []
    for td_text in printed_strings:
        urls.append("http://" + td_text)
        urls.append("https://" + td_text)
    return urls


def check_status_codes(urls):
    status_codes = []
    for sc_check in urls:
        try:
            check = httpx.get(sc_check, timeout=1)
            status_codes.append((sc_check, check.status_code))
        except httpx.RequestError as e:
            status_codes.append((sc_check, -1))  
    return status_codes

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
    status_codes = check_status_codes(urls)
    print_sorted_status_codes(status_codes)

if __name__ == "__main__":
    main()
