from flask import Flask, request, jsonify, render_template, redirect, url_for
from config import Config
from models import db, User
from utils import initialize_utils, get_book_text, split_into_chapters, schedule_email, send_confirmation_email
from books import BOOKS
import stripe
from threading import Thread

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
initialize_utils(app)
stripe.api_key = app.config['STRIPE_SECRET_KEY']

""" @app.before_first_request
def create_tables():
    db.create_all() """

@app.route('/')
def index():
    return render_template('index.html', books=BOOKS)

@app.route('/book/<title>')
def book(title):
    return render_template('book.html', title=title, key=app.config['STRIPE_PUBLIC_KEY'])

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.form
    email = data.get('email')
    friend_emails = request.form.getlist('friend_emails')
    chapters_per_email = data.get('chapters_per_email', 1)
    email_frequency = data.get('email_frequency', 7)
    book_title = data.get('book_title')
    token = data.get('stripeToken')

    if not email or not token or not book_title:
        return jsonify({'error': 'Missing email, payment token, or book title'}), 400

    # Create a new Stripe customer
    try:
        customer = stripe.Customer.create(
            email=email,
            source=token
        )
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400

    # Calculate the total cost
    base_cost = 2.99
    additional_email_cost = 0.99
    free_emails = 2
    total_cost = base_cost + (max(0, len(friend_emails) - free_emails) * additional_email_cost)

    # Create a Stripe subscription (mock implementation, replace with real subscription creation if needed)
    try:
        subscription = stripe.InvoiceItem.create(
            customer=customer.id,
            amount=int(total_cost * 100),  # Stripe amounts are in cents
            currency='usd',
            description=f'Subscription to {book_title}'
        )
        stripe.Invoice.create(customer=customer.id)
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400

    # Create or update the main user in the database
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(
            email=email,
            subscription_active=True,
            chapters_per_email=int(chapters_per_email),
            email_frequency=int(email_frequency),
            stripe_customer_id=customer.id,
            book_title=book_title
        )
        db.session.add(user)
    else:
        user.subscription_active = True
        user.chapters_per_email = int(chapters_per_email)
        user.email_frequency = int(email_frequency)
        user.stripe_customer_id = customer.id
        user.book_title = book_title
    db.session.commit()

    # Store friends' emails in the database
    for friend_email in friend_emails:
        friend = User.query.filter_by(email=friend_email).first()
        if friend is None:
            friend = User(
                email=friend_email,
                subscription_active=True,
                chapters_per_email=int(chapters_per_email),
                email_frequency=int(email_frequency),
                stripe_customer_id=customer.id,  # Link to the same Stripe customer
                book_title=book_title
            )
            db.session.add(friend)
        else:
            friend.subscription_active = True
            friend.chapters_per_email = int(chapters_per_email)
            friend.email_frequency = int(email_frequency)
            friend.stripe_customer_id = customer.id
            friend.book_title = book_title
    db.session.commit()

    # Fetch the book text and split into chapters
    book_id = next((book['id'] for book in BOOKS if book['title'] == book_title), None)
    book_title, chapters_dict = get_book_text(book_id)
    if not book_title or not chapters_dict:
        return jsonify({'error': 'Failed to fetch book text'}), 500

    chapters = list(chapters_dict.values())
    first_chapter = chapters[0] if chapters else "No chapters found."

    # Send confirmation email to the main email and all friends with the first chapter
    recipients = [email] + friend_emails
    print(f"Sending confirmation email to: {recipients}")
    send_confirmation_email(app, recipients, book_title, first_chapter)
    print(f"Sent confirmation email with first chapter to {', '.join(recipients)}")

    # Schedule the email sending
    email_thread = Thread(target=schedule_email, args=(app, user.id, chapters, book_title, recipients))
    email_thread.start()

    return redirect(url_for('success', title=book_title))

@app.route('/success/<title>')
def success(title):
    return render_template('success.html', title=title)

if __name__ == '__main__':
    app.run(debug=True)
