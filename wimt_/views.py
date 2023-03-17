from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from django.contrib import messages
from datetime import date, timedelta


def content(request):
    if request.method == "POST":
      train_no = request.POST.get('floatingInputGrid')
      date_no = request.POST.get('floatingSelectGrid')
      if train_no and date_no:
         Context = {'train_number': request.POST.get('floatingInputGrid'),'date_no':request.POST.get('floatingSelectGrid')}
         
         train_no = request.POST.get('floatingInputGrid')
         
         date_no = request.POST.get('floatingSelectGrid')
      
         date1 = 0
         formateddate1=0
         if date_no == "1":
            date1 = date.today() - timedelta(days=1)
            formateddate1 = date1.strftime("%Y%m%d")


         elif date_no == "2":
              date1 = date.today()
              
              formateddate1=date1.strftime("%Y%m%d")

         else:
            date1 = date.today() + timedelta(days=1)
            formateddate1=date1.strftime("%Y%m%d")

         
         
         path = 'C:\Program Files (x86)\chromedriver.exe'
         option = webdriver.ChromeOptions()
         option.add_argument('headless')
         driver = webdriver.Chrome(path,options=option)
         driver.get(f'https://runningstatus.in/status/{train_no}-on-{ formateddate1 }')
         sample = driver.find_element(By.XPATH,'//table')
         rows = sample.find_elements(By.XPATH,'.//tr')
         anss=[]
         
         for row in rows:
             cell = row.find_elements(By.XPATH,'.//td')
             for cel in cell:
                 cleaned_text = cel.text.replace("\n", " ")
               
                 anss.append(cleaned_text)
         a =driver.find_elements(By.CLASS_NAME,"card-header")
         name=[]
         for element in a:
              if element.tag_name != "small":
                  na=element.text.replace(" | View on Map", "")
                  name.append(na)
               

         for string in name:
            split_list = string.split("\n")
   
         anss.pop()
         ansss= list(filter(None, anss))
        
         ans=[]
         i=0
         while i < len(ansss):
             ans1=[]
             ans1.append(ansss[0+i])
             ans1.append(ansss[1+i])
             ans1.append(ansss[2+i])
             ans1.append(ansss[3+i])
             ans.append(ans1)
             i=i+4

         
         if len(split_list) == 0:
            
            messages.error(request,("Please enter correct train number "))


         return render(request,'home.html',{'split_list':split_list,'ans':ans,'train_no':train_no,'date_no':date_no})
      else:
             messages.success(request,("Please Select Train No And Date!"))
             return render(request,'home.html')

    else:

        
        return render(request,'home.html')


