class Review:
    id: str
    content: str
    cameraID: int
    driverID: str

    def fromJson(self, id: str, content: str, cameraid: int, driverid: str) -> None:
        self.id = id
        self.content = content
        self.cameraID = cameraid
        self.driverID = driverid

