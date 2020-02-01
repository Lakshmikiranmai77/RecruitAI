from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from parsel import Selector
import time
from bs4 import BeautifulSoup
import links as L
import traceback

# database module

import crud

# Run crud module
crud

# database module

driver = webdriver.Chrome()
email="akumar2243@gmail.com"
password="9SCgSNN78S*p2kw"
driver.get("https://www.linkedin.com/login")
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
email_elem = driver.find_element_by_id("username")
email_elem.send_keys(email)
password_elem = driver.find_element_by_id("password")
password_elem.send_keys(password)
driver.find_element_by_tag_name("button").click()
count=0
i=0
for i in range(4):
    for link in L.links[i]:

        # f = open("MyFile"+str(count)+".txt","a+")
        try:
            print(link)
            driver.get(link)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-nav-item")))
            source=driver.page_source
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-nav-item")))
            driver.execute_script("window.scrollTo(0, 1300);")
            time.sleep(5)
        except:
            continue
        print("waited")
        time.sleep(3)
        string = source
        try:
            soup = BeautifulSoup(string, 'html.parser')
            img = soup.findAll("img", {"class": "pv-top-card__photo"})
            profile_pic=img[0]['src']
            about =soup.findAll("p",{"class":"pv-about__summary-text"})
        except:
            print("error in about")
            traceback.print_exc()
        about_data=[]
        try:
            for e in about[0]:
                about_data.append(e.text.strip())
                if '...' in e.text :
                    break
        except:
                print("error in about in loop")
                traceback.print_exc()
        #print(about_data)
        main_about_string=""
        if(len(about_data)>0):
            for e in about_data:
                #f.write(e)
                main_about_string=main_about_string+e

        #exp data
        try:
            expdiv =soup.find("div",{"class":"pv-profile-section-pager ember-view"})
            section=expdiv.find("section",{"class":"pv-profile-section"})
            a=section.find("ul").findAll("li")
        except:
            print("error in exp")
            traceback.print_exc()
            a=[]
        exp=[]
        for e in a:
            data=e.text
            if(data=="/n"):
                continue
            else:
                exp.append(data)

        expdata=[]
        for e in exp:
            ls=e.splitlines()
            for str1 in ls:
                if(str1.isspace() or str1=='' or str1.strip()=='see more' or str1=='...'):
                    continue
                else:
                    expdata.append(str1.strip())
        #print(expdata)
        main_exp_data=""
        for d in expdata:
            #f.write(d)
            main_exp_data=main_exp_data+d.strip()
        try:
            intro=soup.find("div",{"class":"flex-1 mr5"})
            name=intro.ul.li.text.strip()
            title=intro.h2.text.strip()
            ul=intro.findAll("ul")
            location=ul[1].li.text.strip()
        except:
            name=""
            title=""
            location=""
            print("error in name title")
            traceback.print_exc()
        print(name,title,location)
        #f.write(name)
        #f.write(title)
        #f.write(location)
        sel=Selector(text=driver.page_source)
        try:
            skills = sel.xpath('//*[@class="pv-skill-category-entity__name-text t-16 t-black t-bold"]/text()').extract()
            print(skills)
            skills_string = ""
            for s in skills:
                # f.write(s.strip())
                print(s)
                skills_string=skills_string+s
        except:
            print("error in skills")
            traceback.print_exc()
        count+=1
        crud.insertDB(name, location, skills_string, main_exp_data, main_about_string, title)
driver.quit()