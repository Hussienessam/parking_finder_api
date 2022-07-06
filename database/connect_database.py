from firebase_admin import credentials, firestore, initialize_app, storage


def connect():
    cred = credentials.Certificate(
        'database/parkingfinder-589b5-firebase-adminsdk-qp6g6-a3a631e8a6.json')
    default_app = initialize_app(cred, {'storageBucket': 'parkingfinder-589b5.appspot.com' })
    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket, storage
