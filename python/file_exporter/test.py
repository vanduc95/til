#! /usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import glob
import os
import smtplib
import string

now = datetime.datetime.today()  # Get current date

list_of_files = glob.glob('/home/ducnv/file-exporter/test/*')  # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)  # get latest file created in folder
print(latest_file)

newestFileCreationDate = datetime.datetime.utcfromtimestamp(
    os.path.getctime(latest_file))  # get creation datetime of last file

dif = (now - newestFileCreationDate)  # calculating days between actual date and last creation date

logFile = "/home/ducnv/file-exporter/log"  # defining a log file


def checkFolder(dif, now, logFile):
    if dif > datetime.timedelta(
            days=5):  # Check if difference between today and last created file is greater than 5 days

        HOST = "192.16.0.1"  # This must be your smtp server ip
        SUBJECT = "Alert! At least 5 days wthout a new file in folder xxxxxxx"
        TO = "yourmail@yourdomain.com"
        FROM = "noreply@yourdomain.com"
        text = "%s - The oldest file in folder it's %s old " % (now, dif)
        BODY = string.join((
            "From: %s" % FROM, "To: %s" % TO, "Subject: %s" % SUBJECT, "",
            text), "\r\n")
        server = smtplib.SMTP(HOST)
        server.sendmail(FROM, [TO], BODY)
        server.quit()

        file = open(logFile, "a")  # Open log file in append mode

        file.write(
            "%s - [WARNING] The oldest file in folder it's %s old \n" % (
            now, dif))  # Write a log

        file.close()

    else:  # If difference between today and last creation file is less than 5 days

        file = open(logFile, "a")  # Open log file in append mode

        file.write("%s - [OK] The oldest file in folder it's %s old \n" % (
        now, dif))  # write a log

        file.close()


checkFolder(dif, now, logFile)  # Call function and pass 3 arguments defined before