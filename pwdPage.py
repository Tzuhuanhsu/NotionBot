

class pwdPage():
    password: None
    time: None
    RoomID: None
    RoomName: None

    def __init__(self, password, time, RoomID, RoomName) -> None:
        self.password = password
        self.time = time
        self.RoomID = RoomID
        self.RoomName = RoomName

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
                "rich_text": [{"type": "text", "text": {"content":
                                                        '''鐵門密碼 6150#
                                                        住房密碼 {}
                                                        入住房號 {}

                                                        旅客您好!
                                                        以上為您{}的入住密碼，
                                                        （若連續訂房密碼不變）
                                                        請於15: 00後入住，11: 00前退房。
                                                        旅宿為全自助旅宿，客廳為公共空間，敬請降低音量。
                                                        若有任何疑問可以聯絡官方line(ID: @ 508thxrc)，
                                                        祝順心'''
                                                        .format(self.password, self.RoomName, self.time)}}]
            }
        }
