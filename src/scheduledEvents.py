from datetime import date
from db import birthdays

""" Módulo com função que será usada de tempo em tempo (scheduled) """

# Função que consulta o banco e checa se existem aniversariantes no dia corrente
def checkBirthday():
    today = date.today()
    today_dayMonth = today.strftime("%d%m")
    today_year = today.strftime("%Y")

    aniversariantes = birthdays.find({"dayMonth": today_dayMonth})
    response = []
    for i in aniversariantes:
        i["idade"] = int(today_year) - int(i["year"])
        response.append(i)
    return response

