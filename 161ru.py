import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin 
from transliterate import translit 
import time   
import nltk 
from nltk.tokenize import word_tokenize, sent_tokenize 
 
def clean_text(text):
    sentences = sent_tokenize(text)
    cleaned_sentences = []
    
    for sentence in sentences:
        words = word_tokenize(sentence)
        
        cleaned_words = [word for word in words if 'месяц' not in word.lower()]
        
        cleaned_sentence = ' '.join(cleaned_words)
        cleaned_sentences.append(cleaned_sentence)
    
    cleaned_text = ' '.join(cleaned_sentences)
    return cleaned_text 
 
def remove_after_keyword(text, keyword):
     index = text.find(keyword) 
     if index != -1:
        return text[:index]                           
     return text

namber_of_news=1
count_iter = 60
count_for_pars = 2
url_p1 = 'https://161.ru/text/?page='


visited_links = set()

while True:
    url = url_p1 + str(count_for_pars) 
    print(url) 
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', {'href': True})
        news_links = set()  
        for link in links:
            href = link.get('href') 
            print(href)
            if '/text/' in href and href not in visited_links:
                news_links.add(href)  

        for ur_of_news in news_links:  
            ur_of_news = urljoin("https://161.ru", ur_of_news)  
            page_of_news = requests.get(ur_of_news)
            soup_news = BeautifulSoup(page_of_news.content, 'html.parser') 
       
            r= requests.get(ur_of_news) 
            soup = BeautifulSoup(r.text,"lxml")  
            soup21=soup.find("div",class_="columns-wrapper _branding _record")  
            soup22=soup.find("div",class_="inner-columns-wrapper")   
            soup23=soup.find("div",class_="central-right-wrapper")  
            soup24=soup.find("div",class_="central-column-container")   
            soup25=soup.find("div",class_="Y4bXJ") 
            soup26=soup.find("div",class_="omAkj") 
            soup27=soup.find("div",class_="K5mKk") 
            soup28=soup.find("div",class_="_1CRjU") 
            soup29=soup.find("div",class_="jsL2X")
            if soup29 is not None :  
                soup=soup.find("h1",class_="_4K6U+ c24GC dC3nv") 
                soup=soup.find("span") 
                soup12=soup.get_text() 
            else : 
                soup12="Заголовок не найден"
            print(soup12)
            
            soup = BeautifulSoup(r.text,"lxml")    
            soup1=soup.find("div",class_="columns-wrapper _record") 
            soup2=soup.find("div",class_="inner-columns-wrapper") 
            soup3=soup.find("div",class_="central-right-wrapper")
            soup4=soup.find("div",class_="central-column-container") 
            soup5=soup.find("div",class_="Y4bXJ")  
            soup6=soup.find("div",class_="omAkj")  
            soup7=soup.find("div",class_="K5mKk")  
            soup8=soup.find("div",class_="_1CRjU")  
            soup9=soup.find("div",class_="zhFxW")      
            soup9_Link=soup.find("div",class_="_2O7On pIkRz")
            if soup9_Link is not None :
                soup9=soup.find("a",class_="topic-header__item topic-header__time")  
                soup10=soup.find("time",class_="_2DfZq").get("datetime") 
                soup11=soup10.split("T")[0]
            else: 
                soup11="Дата не найдена " 
            print(soup11) 
            
            soup = BeautifulSoup(r.text,"lxml")    
            av1=soup.find("div",class_="columns-wrapper _record")  
            av2=soup.find("div",class_="inner-columns-wrapper")   
            av3=soup.find("div",class_="central-right-wrapper") 
            av4=soup.find("div",class_="central-column-container")  
            av5=soup.find("div",class_="central-column-container")  
            av6=soup.find("div",class_="_3-wIH")  
            av7=soup.find("div",class_="+cjr9")  
            av8=soup.find("div",class_="pj6Gf") 
            
            
            if av8 is not None :     
                 av9=soup.find("p",class_="bda4+").get_text()    
            else : 
                av9="Автор не найден"  
            print(av9) 
             
            soup = BeautifulSoup(r.text,"lxml")   
            teg1=soup.find("div",class_='columns-wrapper _record') 
            teg2=soup.find("main",class_='inner-columns-wrapper') 
            teg3=soup.find("div",class_='central-right-wrapper')  
            teg4=soup.find("div",class_='central-column-container')  
            teg5=soup.find("div",class_='Y4bXJ') 
            teg6=soup.find("div",class_='omAkj')  
            teg7=soup.find("div",class_='K5mKk')  
            teg8=soup.find("div",class_='_1CRjU') 
            teg9=soup.find("div",class_='_OuibJ')  
            teg10=soup.find("ul",class_='_0XrDD') 
            teg11=soup.find("a",class_='R0qz0 NJL+l M5IeQ')      
            if teg11 is not None : 
                teg12=soup.find("a",class_='R0qz0 NJL+l M5IeQ').get("title") 
            else : 
                teg12="Тег не найден "
            print(teg12)
                  




            try:
                if soup_news is not None and teg12!="Тег не найден ":
                    news_contents = soup_news.find_all("p")   

                    if len(news_contents) > 0:    
                        r_teg=teg12  
                        r_teg=translit(r_teg, 'ru', reversed=True) 
                        r_teg=r_teg.split()[0]

                        soup11 = soup11.replace("-", "_")
                        file_name = f"{(soup11)}_161.ru_{r_teg}_{namber_of_news}.txt"
                        file_path = os.path.join(r"C:\Users\fobus\Desktop\dataSet", file_name) 
                 
                        time.sleep(2/100)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            all_paragraphs = "\n".join(p.get_text() for p in news_contents)
                            all_paragraphs = all_paragraphs.split('\n', 1)[1] 

                            sentences = nltk.sent_tokenize(all_paragraphs)
                            cleaned_sentences2 = [s for s in sentences if 'Поделиться' not in s] 
                            cleaned_sentences3 = [s for s in sentences if 'Иллюстрация:' not in s]  
                            cleaned_text = ' '.join(cleaned_sentences2) 
                            cleaned_text = clean_text(cleaned_text) 
                            keyword = "По теме"
                            cleaned_text = remove_after_keyword(cleaned_text, keyword)  
                            

                            f.write(soup12)  
                            f.write("\n")  
                            f.write("\n") 
                            f.write(cleaned_text)  
                            f.write("\n")   
                            f.write("\n")  
                            f.write("Дата :"+soup11)  
                            f.write("\n")  
                            f.write("\n") 
                            f.write("СМИ : 161.ru")  
                            f.write("\n") 
                            f.write("\n")    
                            f.write("Автор :" + av9) 
                            namber_of_news+=1 
                            ann_file_path = os.path.splitext(file_path)[0] + ".ann"
                            open(ann_file_path, "w", encoding="utf-8").close()

            except Exception as e:
                print(f"Exception occurred while processing {ur_of_news}: {e}")
                
            visited_links.add(ur_of_news)  

        count_for_pars += 1  
