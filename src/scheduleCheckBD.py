import sys
import importlib
from datetime import date
from db import birthdays


def checkBirthday():
    today = date.today()
    today_dayMonth = today.strftime("%d%m")
    today_year = today.strftime("%y")
    print(today_dayMonth)
    print(today_year)

    aniversariantes = birthdays.find({"dayMonth": today_dayMonth})
    return aniversariantes
