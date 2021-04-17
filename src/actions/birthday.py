from datetime import date
import schedule
# Tem de importar o db (não ta funcionando)
# from ..config import db 



def checkBirthday():
    today = date.today()
    print(today)
    todayOrganized = today.strftime("%d/%m/%Y")
    print(todayOrganized)
    # db.birthdays.find_one({"birthday":today})

checkBirthday()

# schedule.every().day.at("11:30").do(check_birthdays)

