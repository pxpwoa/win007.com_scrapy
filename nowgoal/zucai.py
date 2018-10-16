# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import pickle
import requests
import pandas as pd
from sqlalchemy import create_engine

import re
with open('league.pickle','rb') as f:
    league = pickle.load(f)
    data  = pd.DataFrame({'leagueName':league})
cnx = create_engine('mysql+pymysql://root:@127.0.0.1:3306/win007?charset=utf8', echo=False)
try:
    data.to_sql(name='zucai_leagues', con=cnx, if_exists='append', index=False)
except:
    print('让球数据数据存入数据库错误!')

league =[]
for id in range(2000):
    r=requests.get('http://info.sporttery.cn/football/history/history_data.php?mid='+str(id))
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        try:
            name = soup.find_all('h2',class_ = "title")[0].text
            soup.find_all('span', class_="win")[0].text
            if name !='':
                league.append(name)

        except:
            continue
with open('league.pickle','wb') as f:
    pickle.dump(league,f)



