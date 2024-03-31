import configparser
import datetime
import random
import threading
import requests
import json
import arrow
from Room import Room
from pwdPage import pwdPage

randomMin = 0
randomMax = 9
doorNumberLength = 6


class notionBot():
    configPath = "config.ini"
    dates = []
    rooms = []
    pwdRecord = []
    config = None

    def __init__(self) -> None:
        pass

    def createRandom(self):
        return random.randint(randomMin, randomMax)

    def crateDoomPwd(self) -> str:
        doorPwdDict = {}
        doorPwd = ""
        for num in range(0, doorNumberLength):
            doorPwdDict[num] = self.createRandom()
        for pwd in doorPwdDict.values():
            doorPwd = doorPwd+str(pwd)
        return doorPwd + "#"

    def initConfig(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(self.configPath)

    def getHeader(self) -> {"Authorization", "Notion-Version", "Content-Type"}:
        return {
            "Authorization": "Bearer " + self.config["notionConfig"]["token"],
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    # 查詢密碼DB

    def queryPWDDatabase(self) -> requests.Response:

        url = self.config["API"]["QueryDataBase"]
        url = url.replace(
            "[database_id]", self.config["notionConfig"]["DBRoomPwd"])
        return requests.post(url=url, headers=self.getHeader())

    # 查詢房間DB
    def queryRoomDBDatabase(self) -> requests.Response:
        url = self.config["API"]["QueryDataBase"]
        url = url.replace(
            "[database_id]", self.config["notionConfig"]["DBRoomID"])
        return requests.post(url=url, headers=self.getHeader())

    # 儲存JSON檔案
    def saveQueryResultsToJson(self, queryPWDDatabaseRequest: requests.Response, fileName: str):
        if queryPWDDatabaseRequest.status_code == 200:
            responseData = queryPWDDatabaseRequest.json()
            # print(queryPWDDatabaseRequest.json())
            with open(fileName, "w", encoding='utf8') as f:
                json.dump(responseData["results"], f)
        else:
            print("request response status code",
                  queryPWDDatabaseRequest.status_code)

    def insertRoomData(self, roomQueryResult):
        for page in roomQueryResult:
            self.rooms.append(
                Room(page["properties"]["房間編號"]["title"][0]["text"]["content"], page["id"]))

    def createPwdPage(self):
        for room in self.rooms:
            for date in self.dates:
                while True:
                    pwd = self.crateDoomPwd()
                    if pwd not in self.pwdRecord:
                        self.pwdRecord.append(pwd)
                        page = pwdPage(pwd, date, room.id)
                        # self.requestAddPage(page)
                        threading.Thread(
                            target=self.requestAddPage, args=(page,)).start()
                        break
                    else:
                        print("repeat pwd", pwd)

    def requestAddPage(self, pwdPage: pwdPage):
        url = self.config["API"]["AddPage"]
        payload = {"parent": {
            "database_id": self.config["notionConfig"]["DBRoomPwd"]},
            "properties": pwdPage.getRequestStruct()}
        res = requests.post(url=url, headers=self.getHeader(), json=payload)

        print(pwdPage.password, "res=", res.status_code)

    # 取得今年的總天數

    def getTotalDay(self, year) -> int:
        if ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
            return 1
        else:
            return 365

    # 取得今年的每一天
    def getThisYearEveryDate(self):
        year = int(datetime.datetime.now().date().strftime("%Y"))
        startDate = "%d-1-1" % year
        totalDay = self.getTotalDay(year)
        dayCount = 0
        while (dayCount < totalDay):
            self.dates.append(arrow.get(startDate).shift(
                days=dayCount).format("YYYY-MM-DD"))
            dayCount += 1


if __name__ == "__main__":
    bot = notionBot()
    bot.initConfig()
    bot.getThisYearEveryDate()
    bot.saveQueryResultsToJson(bot.queryRoomDBDatabase(), "roomResult.json")
    roomQueryResponse = bot.queryRoomDBDatabase()
    if roomQueryResponse.status_code == 200:
        bot.insertRoomData(roomQueryResponse.json()["results"])
    bot.createPwdPage()
