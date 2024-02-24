import requests
from bs4 import BeautifulSoup

def get_website_text(car_name: str):
    google_search_query = '+'.join(car_name.split(' '))
    google_request = requests.get(f'https://www.google.com/search?q=description+of+{google_search_query}')
    google_soup = BeautifulSoup(google_request.text, features='html.parser')
    
    url = [
        x['href']
        for x in google_soup.find_all('a') 
        if '/search' not in x['href'] 
        and 'google' not in x['href'] 
        and x['href'].startswith('/url?q=')
    ][0]

    car_request = requests.get(f'https://www.google.com/{url}')
    car_soup = BeautifulSoup(car_request.text)
    car_text = car_soup.text

    return car_text

if __name__ == '__main__':
    print(get_website_text(input("car name: ")))
    
