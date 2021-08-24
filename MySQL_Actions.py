import datetime
import mysql.connector
from mysql.connector import errorcode
import requests

class MySQL_Actions:
    def __init__(self):
        self.db_settings = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "???",#需要修改密碼
            "db": "ExchangeRateCalc_TW2HK",
            "charset": "utf8"
        }
        self.today = datetime.date.today()
        self.time = datetime.datetime.now()

    def get_req_from_unionpay(self,date):
        URL = f"https://www.unionpayintl.com/upload/jfimg/{date}.json"
        sess = requests.session()
        headers = {
            "Referer": "https://www.unionpayintl.com/hk/rate/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        req = sess.get(URL, headers=headers)
        return req
    
        # save in db
    def insert_data(self, rateInfo):
        try:
            # 建立Connection物件
            conn = mysql.connector.connect(**self.db_settings)
            # 建立Cursor物件
            with conn.cursor() as cursor:
                # 新增資料SQL語法
                command = "INSERT INTO RateRecord(ID, DATE, RateSystem, baseCur, transCur, rateData)VALUES(%s, %s, %s, %s, %s, %s)"
                # for chart in charts:
                cursor.execute(command, (rateInfo["ID"], rateInfo["DATE"], rateInfo["RateSystem"], rateInfo["baseCur"], rateInfo["transCur"], rateInfo["rateData"]))
                # 儲存變更
                conn.commit()
        except Exception as ex:
            print(ex)
        
        cursor.close()
        conn.close()

    def check_data(self):
        try:
        # 建立Connection物件
            conn = mysql.connector.connect(**self.db_settings)
            # 建立Cursor物件
            cursor = conn.cursor()

            cursor.execute("SELECT ID, DATE(DATE),rateData FROM RateRecord;")
            records = cursor.fetchall()
            for item in records:
                print(item)
            conn.close()
        except Exception as ex:
            print(ex)

    def delete_data(self):
        try:
            # 建立Connection物件
            conn = mysql.connector.connect(**self.db_settings)
            # 建立Cursor物件
            with conn.cursor() as cursor:
                # 新增資料SQL語法
                command = "DELETE FROM RateRecord"
                # for chart in charts:
                cursor.execute(command)
                # 儲存變更
                conn.commit()
        except Exception as ex:
            print(ex)
        
        cursor.close()
        conn.close()
    
    def get_today_rate(self):
        try:
            # 建立Connection物件
            conn = mysql.connector.connect(**self.db_settings)
            # print("# 建立conn物件成功")
            # 建立Cursor物件
            cursor = conn.cursor()
            # print("# 建立cursor物件成功")

            # date = self.today - datetime.timedelta(days=14)
            date = self.today
            # print(str(date).replace("-","/") , f"DAY OF WEEK:{date.weekday()}")
            temp_date = date
            time = self.time
            
            # for i in range(3):
            if date.weekday()>4:#Mon:0, FRI:4
                temp_date = date - datetime.timedelta(days=temp_date.weekday()-4)
            elif (date.weekday()>0 and date.weekday()<=4 and ((time.hour!=16 and time.minute<30) or time.hour<16)):
                temp_date = date - datetime.timedelta(days=1)
            elif (date.weekday()==0 and ((time.hour!=16 and time.minute<30) or time.hour<16)):
                temp_date = date - datetime.timedelta(days=3)
            else:
                temp_date = date

            # print(temp_date)
            # print(temp_date.weekday())
            query_date = str(temp_date).replace("-","/") 
            # print(query_date,f"DAY OF WEEK:{temp_date.weekday()}")

            cursor.execute(f"SELECT rateData FROM RateRecord WHERE DATE = '{query_date}';")

            records = cursor.fetchone()
            # for item in records:
                # print(item)
            # print(records[0])
            conn.close()
            return records[0]
        except Exception as ex:
            # print(ex)
            print("連線不成功")
        