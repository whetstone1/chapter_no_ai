import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup  # For HTML parsing
import os
import schedule
import time
from threading import Thread
from models import db, User
import stripe

stripe.api_key = None  # This will be set in the app initialization

def initialize_utils(app):
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

def get_book_text(gutenberg_id):
    try:
        url = f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-h/{gutenberg_id}-h.htm"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        book_title = soup.find('h1').text.strip()
        chapters = {}
        chapter_tags = soup.find_all('a', href=True)
        for tag in chapter_tags:
            if 'chap' in tag['href']:
                chapter_id = tag['href']
                chapter_text = tag.find_next('div').text.strip()
                chapters[chapter_id] = chapter_text
        return book_title, chapters
    except requests.RequestException as e:
        print(f"Error fetching book: {e}")
        return None, {}

def send_email(app, recipients, subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = f"Your Name <{app.config['EMAIL_USER']}>"
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        print(f"Connecting to SMTP server: {app.config['SMTP_SERVER']}:{app.config['SMTP_PORT']}")
        with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
            server.starttls()
            print(f"Logging in as {app.config['EMAIL_USER']}")
            server.login(app.config['EMAIL_USER'], app.config['EMAIL_PASS'])
            print(f"Sending email to {', '.join(recipients)}")
            server.sendmail(message["From"], recipients, message.as_string())
        print(f"Email sent to {', '.join(recipients)}")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_confirmation_email(app, recipients, book_title, first_chapter):
    subject = f"Subscription Confirmation for {book_title}"
    body = f"Thank you for subscribing to {book_title}. You will start receiving the chapters as per your subscription settings.\n\nHere is your first installment:\n\n{first_chapter}"
    send_email(app, recipients, subject, body)

def split_into_chapters(book_text):
    chapters = book_text.split('Chapter ')
    chapters = ["Chapter " + chapter for chapter in chapters if chapter.strip() != '']
    return chapters

def send_chapter_installments(app, chapters, recipients, book_title, chapters_per_email):
    num_chapters = len(chapters)
    num_emails = int(num_chapters / chapters_per_email) + (num_chapters % chapters_per_email > 0)

    for i in range(num_emails):
        start_index = i * chapters_per_email
        end_index = min((i + 1) * chapters_per_email, num_chapters)
        chapter_text = "\n\n".join(chapters[start_index:end_index])
        subject = f"Chapters {start_index+1} to {end_index} - {book_title}"
        send_email(app, recipients, subject, chapter_text)

def schedule_email(app, user_id, chapters, book_title, recipients):
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            return

        def job():
            send_chapter_installments(app, chapters, recipients, book_title, user.chapters_per_email)

        schedule.every(user.email_frequency).days.do(job)

        while user.subscription_active:
            schedule.run_pending()
            time.sleep(1)
