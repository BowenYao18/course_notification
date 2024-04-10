import requests
import time
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_notification(email, password, recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, recipient, text)
    server.quit()


def fetch_course_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully fetched course info.")
        html_content = response.text
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the "Section Max Enrollment" data
        max_enrollment_text = soup.find('b', string="Section Max Enrollment: ")
        # Find the "Section Enrolled: " data
        enrollment_text = soup.find('b', string="Section Enrolled: ")

        # Get the next sibling (which should be the number)
        max_enrollment_number = max_enrollment_text.next_sibling
        enrollment_number = enrollment_text.next_sibling

        # Extract just the number using regular expression
        if max_enrollment_number:
            match = re.search(r'\d+', max_enrollment_number)
            if match:
                max_enrollment_number = int(match.group())
        if enrollment_number:
            match = re.search(r'\d+', enrollment_number)
            if match:
                enrollment_number = int(match.group())

        print("Section Max Enrollment:", max_enrollment_number)
        print("Section Enrolled: ", enrollment_number)

        if max_enrollment_number > enrollment_number:
            print("The course has empty seats!")
            # Define your email, password, recipient, subject and body
            email = "SENDER EMAIL HERE"
            password = "SENDER PASSWORD HERE"
            recipient = "RECIPIENT EMAIL HERE"
            subject = "Course Seat Available"
            body = "There are empty seats available in the course."
            send_notification(email, password, recipient, subject, body)
        else:
            print("The course is full!")

    else:
        print("Failed to fetch course info. Status code:", response.status_code)


def main():
    URL = "YOUR URL HERE"
    while True:
        fetch_course_info(url)
        print("Waiting for 60 minutes...")
        time.sleep(3600)  # Wait for 3600 seconds (60 minutes)


if __name__ == "__main__":
    main()
