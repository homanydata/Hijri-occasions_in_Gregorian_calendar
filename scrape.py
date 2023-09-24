from bs4 import BeautifulSoup
import requests
from lookups import Links, Errors, get_hijri_number
import re
import datetime

def get_soup_body(link):
    html_file = requests.get(link)
    soup = BeautifulSoup(html_file.content, features="lxml")
    return soup.body

def parallel_gregorian_date(today_hijri, goal_hijri):
    # difference is surely not more than a month since all what we are getting is this hijri month occasions 
    interval = int(goal_hijri) - int(today_hijri)
    today_gregorian = datetime.datetime.now().date()
    goal_gregorian = today_gregorian + datetime.timedelta(days=interval)
    
    return goal_gregorian

def get_today_hijri():
    soup = get_soup_body(Links.MAIN_PAGE)
    div = soup.find("div",{"class":"main-content-carousel-title"})
    text_full_date = div.select("span")[1].text.strip()

    numbers = re.findall(r'\d+', text_full_date)
    
    if len(numbers) >= 4:
        # extract the 3rd number
        third_number = numbers[2]
        # find the index of the 3rd number in the text
        third_number_index = text_full_date.index(third_number)
        # find the index of the 4th number in the text
        fourth_number_index = text_full_date.index(numbers[3])
        # extract the text between the 3rd and 4th numbers, which is month name
        month = text_full_date[third_number_index + len(third_number):fourth_number_index].strip()
        month = 'ربيع الاول'
        result = {'day':third_number, 'month':month}
        return result
    else:
        print(Errors.Not_Full_Date_Format)

def get_month_occasions(hijri_date):
    hijri_month = hijri_date['month']
    soup = get_soup_body(link=Links.HIJRI_MONTH_PAGE(get_hijri_number(hijri_month)))
    occasions_list = soup.find_all('span', class_='label label-default')

    result = "مناسبات هالشهر:"
    i = 0
    while i < len(occasions_list):
        hijri_day = occasions_list[i].text
        occasion_text = occasions_list[i+1].text
        gregorian_date = parallel_gregorian_date(today_hijri=hijri_date['day'], goal_hijri=hijri_day)
        result += f"\n{hijri_day}-{hijri_month} ({gregorian_date}): {occasion_text}"
        i += 2
    return result
