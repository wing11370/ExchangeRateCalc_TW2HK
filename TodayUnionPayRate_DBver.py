from MySQL_Actions import MySQL_Actions
import datetime
import math

class Flow_DBver():
    def __init__(self):
        self.MySQL_connection = MySQL_Actions()
        self.rate = self.MySQL_connection.get_today_rate()

        if self.rate == None: print("本日銀聯匯率未更新")
        else:print(f"本日銀聯匯率 :{self.rate}\n港幣$ 1 = 新台幣${str(1/float(self.rate))}")

        print("香港的金融卡在台灣ATM提款，每一筆需要 港幣$20手續費\n每一筆提款最高可領取 新台幣$20000")


    def save_in_json(self,req_to_json, date, i=""):
        output_json = open(f"Daily_rate/{date}.json","w")
        print(f"{i},{date}.json done")
        output_json.write(str(req_to_json))
        output_json.close()

    def flow_save(self):
        for i in range(100):
            date = str(self.MySQL_connection.today - datetime.timedelta(days=i)).replace("-","")
            req = self.MySQL_connection.get_req_from_unionpay(date)

            if req.status_code == 200:
                print("connected")
                req_to_json = req.json()
                self.save_in_json(req_to_json, date, i)

                for i in range(len(req_to_json['exchangeRateJson'])):
                    if req_to_json['exchangeRateJson'][i]["baseCur"]=="HKD" and req_to_json['exchangeRateJson'][i]["transCur"]=="TWD":
                        rate = (req_to_json['exchangeRateJson'][i]["rateData"])
                        break
                
                rateInfo = {"ID":date+"_UNIONPAY_HKD_TWD", "DATE":date, "RateSystem":"UnionPay", "baseCur":"HKD", "transCur":"TWD", "rateData":rate}
                
                self.MySQL_connection.insert_data(rateInfo)
    
    def flow_check_data(self):
        self.MySQL_connection.check_data()
    
    def flow_delete_data(self):
        self.MySQL_connection.delete_data()
    
    def flow_run(self):
        start = 1
        while start:
            try:
                ntd = int(input("請輸入需要提領的新台幣$："))
                hkd = int(ntd)*float(self.rate)
                print(f"TW${ntd} = HK${hkd}")
                times=math.ceil(ntd/20000)
                print(f"共需要提領次數:",times)
                fee = 20*times
                print(f"手續費共港幣${fee}")
                cost = round(hkd+ fee,1)
                print(f"總金額港幣${cost}\n====================")
                
                again=1
                while again:
                    contin=input("要執行新的計算嗎？ 0:離開；1:繼續")
                    if contin=="0":
                        start=0
                        again=0
                        break
                    elif contin=="1":
                        start=1
                        again=0
                        continue
                    else:print("請輸入 0或1")
            except:print("請輸入整數")