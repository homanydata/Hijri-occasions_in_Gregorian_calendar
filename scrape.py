from bs4 import BeautifulSoup
import requests
import lxml
from lookups import Links, Errors, get_hijri_number, next_hijri_month
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
        months = [month]
        
        # this condition checks if the hijri month ends sooner than the gregorian, so we will need to check next hijri month also
        if parallel_gregorian_date(today_hijri=third_number, goal_hijri=25).month == datetime.datetime.now().month:
            months.append(next_hijri_month(month))
        result = {'day':int(third_number), 'months':months}
        return result
    else:
        print(Errors.Not_Full_Date_Format)

def get_month_occasions(hijri_date):
    result = ":مناسبات هالشهر"
    hijri_months = hijri_date['months']
    # get current hijri month number, use it to get the suitable link
    soup = get_soup_body(link=Links.HIJRI_MONTH_PAGE(get_hijri_number(hijri_months[0])))
    # list of day-occasion elements
    occasions_list = soup.find_all('span', class_='label label-default')
    i = 0
    while i < len(occasions_list):
        hijri_day = int(occasions_list[i].text)
        if hijri_day > hijri_date['day']:
            occasion_text = occasions_list[i+1].text
            gregorian_date = parallel_gregorian_date(today_hijri=hijri_date['day'], goal_hijri=hijri_day)
            result += f"\n({hijri_day}- {hijri_months[0]}) ({gregorian_date}): {occasion_text}"
        # increment 2 since we're reading them 2 by 2, 1st is date & 2nd is occasion title
        i += 2
    
    if len(hijri_date['months']) == 1:
        return result

    # next hijri month
    soup = get_soup_body(link=Links.HIJRI_MONTH_PAGE(get_hijri_number(hijri_months[1])))
    occasions_list = soup.find_all('span', class_='label label-default')
    i = 0
    while i < len(occasions_list):
        hijri_day = int(occasions_list[i].text)
        occasion_text = occasions_list[i+1].text
        gregorian_date = parallel_gregorian_date(today_hijri= (hijri_date['day'] - 29), goal_hijri=hijri_day)
        # subtract 29 from today_hijri since we need to count for days left in this month
        result += f"\n({hijri_day} - {hijri_months[1]}) ({gregorian_date} او {gregorian_date.day+1}): {occasion_text}"
        # similar to code for first month, except for the condition on occ_day > today, & today_hijri value passed
        i += 2
    return result
