#爬蟲程式，抽取當天銀聯匯率

from urllib.error import HTTPError
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as soup
import math
def start():
    def get_links(url):
        result = requests.get(url)
        page = result.text
        doc = soup(page)
        links = [element.get("href") for element in doc.find_all("a")]
        return links

    def getPrice(url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
            return None
        try:
            Obj = soup(html,"html.parser")
            # titles = Obj.find("b")
            titles = [element for element in Obj.find("b")]
        except AttributeError as e:
            return None
        return titles

    url="https://www.hkrates.com/cardrate/unionpay/twd.html"
    titles = getPrice(url)
    if titles == None: print("None")
    else:print(f"本日銀聯匯率 :{titles[0]}\n港幣$ 1 = 新台幣${str(1/float(titles[0]))}")
    print("香港的金融卡在台灣ATM提款，每一筆需要 港幣$20手續費\n每一筆提款最高可領取 新台幣$20000")
    
    start = 1
    while start:
        try:
            ntd = int(input("請輸入需要提領的新台幣$："))
            hkd = int(ntd)*float(titles[0])
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