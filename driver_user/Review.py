from datetime import datetime


class Review:
    id: str
    content: str
    date: str
    cameraID: int
    driverID: str


    def fromJson(self, id: str, content: str, date: str, cameraid: int, driverid: str) -> None:
        self.id = id
        self.content = content
        self.date = date
        self.cameraID = cameraid
        self.driverID = driverid

