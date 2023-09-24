from scrape import get_month_occasions, get_today_hijri
from lookups import next_hijri_month, get_hijri_number

today_hijri_date = get_today_hijri()
result_text = get_month_occasions(today_hijri_date)
print(result_text)
