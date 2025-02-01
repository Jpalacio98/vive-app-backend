import os

class Config:
    FIREBASE_CREDENTIALS = os.path.join('utils', 'serviceAccountKey.json')
    STRIPE_KEY= os.getenv('stripe_secret_key')
