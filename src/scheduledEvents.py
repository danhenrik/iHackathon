from datetime import date
from db import birthdays


def checkBirthday():
    today = date.today()
    today_dayMonth = today.strftime("%d%m")
    today_year = today.strftime("%Y")

    aniversariantes = birthdays.find({"dayMonth": today_dayMonth})
    for i in aniversariantes:
        i["idade"] = int(today_year) - int(i["year"])
    return aniversariantes


def checkReminder():
    print("Rodou uma vez")
