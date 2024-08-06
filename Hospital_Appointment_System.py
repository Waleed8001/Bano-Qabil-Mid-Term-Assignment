import requests
import datetime
import smtplib

url1 = "https://api.sheety.co/468fa27b225c199db6181089b7355d81/hospitalAppointmentScheduler/hospital"
url2 = "https://api.sheety.co/468fa27b225c199db6181089b7355d81/hospitalAppointmentScheduler/hospital"
url3 = "https://api.sheety.co/468fa27b225c199db6181089b7355d81/hospitalAppointmentScheduler/hospital"
url4 = "https://api.sheety.co/468fa27b225c199db6181089b7355d81/hospitalAppointmentScheduler/hospital"

GMAIL = 'waleedkamal801@gmail.com'
GMAILPASSWORD = 'kuep ufnk icfr pmwi'
GMAILAPI = 'smtp.gmail.com'
GMAILPORT = 587
def take():
    a = requests.get(url = url1)
    b = a.json().get('hospital',[])
    return b

def mail(GMAILTO,subject,message):
    with smtplib.SMTP(GMAILAPI,GMAILPORT) as has:
        has.starttls()
        has.login(GMAIL,GMAILPASSWORD)
        send = f"SUbject:{subject}\n\n{message}"
        has.sendmail(GMAIL,GMAILTO,send)
        has.quit()

# For Faisal Bhai
def update_sheet_for_Not_visiting(i_id):
    o = i_id
    hospitalAppointmentScheduler = {
        "hospital":{
            'status':"Last Warning"
        }
    }

    update = requests.put(url = f"{url3}/{o}",json = hospitalAppointmentScheduler)
    update.raise_for_status()

def update_sheet_for_Registered(i_id):
    o = i_id
    hospitalAppointmentScheduler = {
        "hospital":{
            'status':"Not Visited"
        }
    }

    update = requests.put(url = f"{url3}/{o}",json = hospitalAppointmentScheduler)
    update.raise_for_status()    

# For Faisal Bhai
def delete_detail_of_visited_person(i_id):
    i = i_id
    del_data = requests.delete(url=f"{url4}/{i}")
    del_data.raise_for_status()

take = take()
date = datetime.datetime.now()
date2 = date.strftime("%m/%d/%Y")
for i in take:
    if i['dateOfAppointment'] == date2 and i['status'] == "Registered":
        subject = "Hospital Appointment"
        message = f"""Assalamualaikum {i['patientsName']},
You came in our hospital in {i['dateTakenOn']} and have taken appointment for {i['dateOfAppointment']} for the desease of {i['disease']} and the age  of patient is {i['age']}. So please visit on the desired timing {i['timing']}.
Thank you.

For any query please call:
03242923319"""
        mail(i['email'],subject,message)
        update_sheet_for_Registered(i['id'])

    # For Faisal Bhai
    if i['status'] == "Visited":
        delete_detail_of_visited_person(i['id'])

    # For Faisal Bhai
    if i['status'] == "Not Visited":
        subject = "Hospital Appointment"
        message = f"""Assalamualaikum {i['patientsName']},
You came in our hospital in {i['dateTakenOn']} and have taken appointment for {i['dateOfAppointment']} for the desease of {i['disease']} and the age  of patient is {i['age']} but you still not visited in the department. It is your last warning otherwise your registeration will be cancelled. If you want to cancel registration so please call in the given number. So please visit on the desired timing {i['timing']}.If you want to cancel your registration so please call on the given number.
Thank you.

For any query please call:
03242923319"""
        update_sheet_for_Not_visiting(i['id'])
        mail(i['email'],subject,message)
