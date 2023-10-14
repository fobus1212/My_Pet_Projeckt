import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin 
import re  
from transliterate import translit 
import time  

namber_of_news=1
count_iter = 10
count_for_pars = 1
url_p1 = 'https://lenta.ru/parts/news/'
url_p2 = "/"

visited_links = set()

for i in range(count_iter):
    url = url_p1 + str(count_for_pars) + url_p2
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', {'href': True})
        news_links = set()  
        for link in links:
            href = link.get('href') 
            print(href)
            if '/news/' in href and href not in visited_links:
                news_links.add(href)  

        for ur_of_news in news_links:  
            ur_of_news = urljoin("https://lenta.ru/", ur_of_news)  
            page_of_news = requests.get(ur_of_news)
            soup_news = BeautifulSoup(page_of_news.content, 'html.parser') 
       
            r= requests.get(ur_of_news) 
            soup = BeautifulSoup(r.text,"lxml")  
            soup=soup.find("div",class_="topic-body _news")  
            if soup is not None :  
                soup=soup.find("h1",class_="topic-body__titles") 
                soup=soup.find("span", class_="topic-body__title") 
                soup12=soup.get_text() 
            else : 
                soup12="Заголовок не найден"
            print(soup12)
            
            soup = BeautifulSoup(r.text,"lxml")    
            soup1=soup.find("div",class_="topic-page__wrap js-topic") 
            soup2=soup.find("div",class_="topic-page g-application _news") 
            soup3=soup.find("div",class_="topic-page__container")
            soup4=soup.find("div",class_="topic-page__header") 
            soup5=soup.find("div",class_="topic-header _news")  
            soup6=soup.find("div",class_="topic-header__info")  
            soup7=soup.find("div",class_="topic-header__left-box")  
            soup8=soup.find("div",class_="topic-header__item")   
            soup8_Link=soup.find("div",class_="topic-header__item")
            if soup8_Link is not None :
                soup9=soup.find("a",class_="topic-header__item topic-header__time").get("href")  
            else: 
                soup9="Дата не найдена " 
            print(soup9) 
            
            soup = BeautifulSoup(r.text,"lxml")    
            av1=soup.find("div",class_="topic-page__content _news")  
            av2=soup.find("div",class_="topic-footer js-topic-footer")   
            av3=soup.find("div",class_="topic-page__info") 
            av3=soup.find("div",class_="topic-authors") 
            av4_Links=soup.find("a",class_="topic-authors__author") 
            if av4_Links is not None :     
                av4=soup.find("a",class_="topic-authors__author").get_text()   
            else : 
                av4="Автор не найден"  
            print(av4) 
             
            soup = BeautifulSoup(r.text,"lxml")   
            teg1=soup.find("div",class_='layout__container') 
            teg2=soup.find("main",class_='topic-page__wrap js-topic') 
            teg3=soup.find("div",class_='rubric-header')  
            teg4=soup.find("div",class_='rubric-header__title-wrap')  
            teg5=soup.find("div",class_='rubric-header__title') 
            if teg5 is not None : 
                teg5=soup.find("div",class_='rubric-header__title').get_text() 
            else : 
                teg5="Тег не найден "
            print(teg5)
                  




            try:
                if soup_news is not None and teg5!="Тег не найден ":
                    news_contents = soup_news.find_all("p")   

                    if len(news_contents) > 0: 
                        r_date=soup9 
                        r_date=r_date[1:]   
                        r_date=r_date[:-1]   
                        r_teg=teg5    
                        r_teg=r_teg.split()[0]
                        r_teg=translit(r_teg, 'ru', reversed=True)
                        file_name = f"{re.sub(r'/', '_', r_date)}_Lenta.ru_{r_teg}_{namber_of_news}.txt"
                        file_path = os.path.join(r"C:\Users\fobus\Desktop\dataSet", file_name)  
                        with open(file_path, "w", encoding="utf-8") as f:
                            all_paragraphs = "\n".join(p.get_text() for p in news_contents)
                            all_paragraphs = all_paragraphs.split('\n', 1)[1]   
                            f.write(soup12)  
                            f.write("\n")  
                            f.write("\n") 
                            f.write(all_paragraphs)  
                            f.write("\n")   
                            f.write("\n")  
                            f.write("Дата :"+soup9)  
                            f.write("\n")  
                            f.write("\n") 
                            f.write("СМИ : Lenta.ru")  
                            f.write("\n") 
                            f.write("\n")    
                            f.write("Автор :" + av4) 
                            namber_of_news+=1   
                            ann_file_path = os.path.splitext(file_path)[0] + ".ann"
                            open(ann_file_path, "w", encoding="utf-8").close()
                            time.sleep(1)
            except Exception as e:
                print(f"Exception occurred while processing {ur_of_news}: {e}")
                
            visited_links.add(ur_of_news)  
        count_for_pars += 1 