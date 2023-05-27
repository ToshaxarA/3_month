# Парсинг данных pip install lxml request beatutifulsoup4

from bs4 import BeautifulSoup
import requests

# def parsing_aki():
#     url = 'https://akipress.org/'
#     responce = requests.get(url)
#     print(responce)

#     soup = BeautifulSoup(responce.text)
#     news = soup.find_all('a', class_='newslink')
#     # for n in news:
#     #     print(f"{n.text}\n")
#     a=0
#     j=0
#     for n in news:
#         j+=1
#         with open('news.txt', 'a+', encoding='utf-8') as news_file:
#             news_file.write(f"{j}) {n.text}\n")
        
            


#     f = open('text_news.txt', 'w', encoding='utf-8')
#     for n in news:
#         stroka = n.text
#         a+=1
#         f.write(f"{str(a)}. {stroka}\n")
#     f.close()
    
    # with open('text_news.txt', 'w', encoding='utf-8') as file:
    #     for n in news:
    #         write(index + n.news)
def parsing_currency():
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for usd in currency[0:2]:
        print(usd.text)
    print("==============")
    for eur in currency[2:4]:
        print(eur.text)
    print("==============")
    for rub in currency[4:6]:
        print(rub.text)
    print("==============")
    for kzt in currency[6:8]:
        print(kzt.text)
    print("==============")

parsing_currency()