import user_operations.user_queries_app as user_queries
import requests
import cv2
import numpy as np
import imutils
from flask import request


def mock(db, bucket,storage):
    camera_id = request.json['id']
    capacity = request.json['capacity']
    mock_garage = request.json['mock_garage']

    url = "http://192.168.1.8:8080/shot.jpg"
    while True:
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=1000, height=1800)
        cv2.imshow("life_stream", img)
        if cv2.waitKey(1) == ord('s'):
            cv2.imwrite(filename='snap.jpg', img=img)
            blob = bucket.blob(camera_id+'.jpg')
            image_data = 'snap.jpg'
            blob.upload_from_filename(
                image_data,
                content_type='image/jpg'
            )
            image_url = storage.child(camera_id + '.jpg').get_url(None)
            snap = {'cameraID': camera_id, 'capacity': capacity, 'path': image_url}
            return user_queries.update_snaps(db, snap, mock_garage)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    return "success"

