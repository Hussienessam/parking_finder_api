import pyrebase as pyrebase


appConfig = {

    "apiKey": "AIzaSyDK1_W7qFs9U5zilY7h6RzEeBwlLF1GD18",

    "authDomain": "parkingfinder-589b5.firebaseapp.com",

    "databaseURL": "https://parkingfinder-589b5-default-rtdb.firebaseio.com",

    "projectId": "parkingfinder-589b5",

    "storageBucket": "parkingfinder-589b5.appspot.com",

    "messagingSenderId": "955666530777",

    "appId": "1:955666530777:web:6a4616153006f7644219c8",

    "measurementId": "G-Q5L0X4WDMK"
}


def connect():
    firebase = pyrebase.initialize_app(appConfig)
    auth = firebase.auth()
    db2 = firebase.database()
    return auth
