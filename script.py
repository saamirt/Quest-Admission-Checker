from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
import os
import time
while True:
    QUESTUSER = raw_input("Enter Quest Username: ")
    QUESTPASS = raw_input("Enter Quest Password: ")
    EMAILUSER = raw_input("Enter Gmail: ")
    EMAILPASS = raw_input("Enter Gmail Password: ")

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAILUSER, EMAILPASS)
        server.close()
    except Exception, e:
        os.system('cls')
        print("Incorrect Gmail Login\n")
        continue

    print ("Loading Admission Status...")
    
    browser = webdriver.PhantomJS()
    wait = WebDriverWait(browser, 100)

    while True:
        try:
            browser.get('https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?PORTALPARAM_PTCNAV=HC_SSS_STUDENT_CENTER&EOPP.SCNode=SA&EOPP.SCPortal=ACADEMIC&EOPP.SCName=CO_EMPLOYEE_SELF_SERVICE&EOPP.SCLabel=Self%20Service&EOPP.SCPTfname=CO_EMPLOYEE_SELF_SERVICE&FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_SSS_STUDENT_CENTER&IsFolder=false&')
            username = browser.find_element_by_name("userid")
            password = browser.find_element_by_name("pwd")
            username.send_keys(QUESTUSER)
            password.send_keys(QUESTPASS)
            browser.find_element_by_name("Submit").click()
            status = "Application"
            while (status == "Application"):
                browser.switch_to_frame("ptifrmtgtframe");
                element = wait.until(EC.presence_of_element_located((By.ID, "PROGRAM$0")))
                browser.find_element_by_name("PROGRAM$0").click()
                element = wait.until(EC.presence_of_element_located((By.ID, "STATUS$0")))
                status = browser.find_element_by_name("STATUS$0").text
                os.system('cls')
                print ("ADMISSION STATUS: " + status.upper())
                print ("Updated at: " + time.strftime("%x %I:%M:%S %p"))
                browser.refresh()
            subject = 'WATERLOO ADMISSION STATUS: ' + status.upper()
            body = 'The python webscraping application found that your admission status has changed to: ' + status
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(EMAILUSER, EMAILPASS)
            server.sendmail(EMAILUSER, EMAILUSER, message)
            server.close()
        except Exception, e:
            if "Unable to switch to frame" in str(e):
                os.system('cls')
                print ("Incorrect Quest Login\n")
                continue
            print ("\nSomething went wrong")
            print e
            print ("Program is restarting...")
