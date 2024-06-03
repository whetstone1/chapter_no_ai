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

import requests
from bs4 import BeautifulSoup

def get_book_text(book_id):
    try:
        # Fetch the HTML content of the book
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the book title
        book_title = soup.find('h1').get_text(strip=True)
        print(f"Book title: {book_title}")
        chapters = {}

        # Find all chapter tags by div with class 'chapter', a tags with specific href patterns
        chapter_divs = soup.find_all('div', class_='chapter')
        chapter_a_tags_link2HCH = soup.find_all('a', href=lambda x: x and x.startswith('#link2HCH'))
        chapter_a_tags_chapter = soup.find_all('a', href=lambda x: x and x.startswith('#Chapter_'))

        # Process div.chapter tags
        if chapter_divs:
            print(f"Found {len(chapter_divs)} chapter markers using 'div.chapter'")
            for i, tag in enumerate(chapter_divs):
                if tag.find('p'):  # Ensure the chapter has <p> tags
                    chapter_title = f"Chapter {i+1}"
                    chapter_content = tag.get_text(separator="\n").strip()
                    chapters[chapter_title] = chapter_content
                    print(f"Extracted content for {chapter_title}: {chapter_content[:500]}...")  # Print the first 500 characters

        # Process a[href^="#link2HCH"] tags
        elif chapter_a_tags_link2HCH:
            print(f"Found {len(chapter_a_tags_link2HCH)} chapter markers using 'a[href^=\"#link2HCH\"]'")
            for i, tag in enumerate(chapter_a_tags_link2HCH):
                chapter_title = f"Chapter {i+1}"
                chapter_content = []

                # Collect all text nodes until the next chapter marker
                next_node = tag.find_next_sibling()
                while next_node and not (next_node.name == 'a' and next_node.get('href') and next_node['href'].startswith('#link2HCH')):
                    if next_node.name and next_node.get_text(strip=True):
                        chapter_content.append(next_node.get_text(strip=True))
                    next_node = next_node.find_next_sibling()

                chapters[chapter_title] = '\n'.join(chapter_content)
                print(f"Extracted content for {chapter_title}: {chapters[chapter_title][:500]}...")  # Print the first 500 characters

        # Process a[href^="#Chapter_"] tags
        elif chapter_a_tags_chapter:
            print(f"Found {len(chapter_a_tags_chapter)} chapter markers using 'a[href^=\"#Chapter_\"]'")
            for i, tag in enumerate(chapter_a_tags_chapter):
                chapter_title = f"Chapter {i+1}"
                chapter_content = []

                # Collect all text nodes until the next chapter marker
                next_node = tag.find_next_sibling()
                while next_node and not (next_node.name == 'a' and next_node.get('href') and next_node['href'].startswith('#Chapter_')):
                    if next_node.name and next_node.get_text(strip=True):
                        chapter_content.append(next_node.get_text(strip=True))
                    next_node = next_node.find_next_sibling()

                chapters[chapter_title] = '\n'.join(chapter_content)
                print(f"Extracted content for {chapter_title}: {chapters[chapter_title][:500]}...")  # Print the first 500 characters

        else:
            print("No chapter markers found.")
            return book_title, chapters

        return book_title, chapters
    except requests.RequestException as e:
        print(f"Error fetching book: {e}")
        return None, None

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
