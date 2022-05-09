from firebase_admin import credentials, firestore, initialize_app

def connect():
    cred = credentials.Certificate('parkingfinder-589b5-firebase-adminsdk-qp6g6-a3a631e8a6.json')
    default_app = initialize_app(cred)
    db = firestore.client()
