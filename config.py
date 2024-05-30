import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY') or 'pk_test_51OUvysHhgctZNdPDi6bNGWG9HsyEouKKrxCKbtKwtVC9H7aWrrO7aZ87dtCOzK73ihOd8w8NtmS6Y2XQn9yXH2RO00UvcewJKi'
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_51OUvysHhgctZNdPDGjSLNXDPzF7eyJTR2z2giFPygkFwLMWkuNkMqVFiHxyKXNojKTpFjVQf0JcVbGuCF1wBjv7B00U5KPx8ZA'
    EMAIL_USER = os.environ.get('EMAIL_USER') or 'cole.whetstone@gmail.com'
    EMAIL_PASS = os.environ.get('EMAIL_PASS') or 'glge ytbw slvf rall'
    SMTP_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))