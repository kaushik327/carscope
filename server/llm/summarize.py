import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def get_website_text(car_name: str):
    splitter = car_name.split()
    two_words = {'Aston Martin', 'Land Rover', 'MINI Cooper'}
    body_type = {'Sedan', 'Hatchback', 'SUV', 'Coupe', 'Convertible', 'Wagon', 'Minivan', 'Van', 'Conv.'}
    start = 1
    if(' '.join(splitter[:2]) in two_words):
      brand_name = f"{splitter[0].lower()}-{splitter[1].lower()}"
      start+=1
    else:
      brand_name = splitter[0].lower()

    model_name = ''
    
    '-'.join(splitter[start: -2]).lower()

    for i in range(start, len(splitter) - 1):
      if(splitter[i] in body_type):
        break
      model_name+=splitter[i].lower() + '-'
    model_name = model_name[:-1]

    year = splitter[-1]

    car_request = requests.get(f'https://www.kbb.com/{brand_name}/{model_name}/{year}')
    car_soup = BeautifulSoup(car_request.text)
    car_text = car_soup.text
    return car_text

def load_qa_pipeline():
    return pipeline("question-answering", model="deepset/tinyroberta-squad2")

def load_summay_pipeline():
    return pipeline("summarization", model="google-t5/t5-base", tokenizer="google-t5/t5-base", framework="pt")
    

if __name__ == '__main__':
    print(get_website_text(input("car name: ")))
    
