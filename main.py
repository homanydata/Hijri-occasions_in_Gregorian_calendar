import PySimpleGUI as sg
import pyperclip
from scrape import get_month_occasions, get_today_hijri
import requests

def get_result():
    try:
        today_hijri_date = get_today_hijri()
        result = get_month_occasions(today_hijri_date)
    except requests.exceptions.ConnectionError:
        result = "Please check your internet connection"
    except Exception as e:
        result = "This error happened while trying to get the data needed:\n" + str(e)
    return result

sg.theme('DarkTeal9')

layout = [
    [sg.Button('Generate'), sg.Exit()]
]

def create_copy_layout(result: str):
    sg.set_options(font=('Any', 14))
    result_text = [
        [sg.Text(result, justification='right')]
    ]
    layout = [
        [sg.Column(result_text, element_justification='right')],
        [sg.Button('Copy'), sg.Button('Exit')]
    ]
    return layout

window = sg.Window('Simple data entry form', layout)

result = ""

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Generate':
        result = get_result()
        window.close()
        layout = create_copy_layout(result)
        window = sg.Window('Result', layout)

    if event == 'Copy':
        pyperclip.copy(result)
window.close()
