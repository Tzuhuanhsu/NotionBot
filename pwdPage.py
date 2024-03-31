class pwdPage():
    password: None
    time: None
    RoomID: None

    def __init__(self, password, time, RoomID) -> None:
        self.password = password
        self.time = time
        self.RoomID = RoomID
        pass

    def getRequestStruct(self):
        return {
            "title": {
                "title": [{"type": "text", "text": {"content": self.password}}]

            },
            "Date": {
                "date": {"start": self.time, "end": None}
            },
            "Room": {
                "relation": [{"id": self.RoomID}]
            },
            "備註":
            {
                "rich_text": [{"type": "text", "text": {"content": "親愛的房客您好,您於 2024-04-01 預定房間，我們提供您大門密碼：#12345 以及房間密碼: #123456, 如有入住任何問題，請聯絡  Line小管家:@123456, 或撥打電話:09-32-756-682"}}]
            }
        }
