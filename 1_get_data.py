from lxml import html
import requests
from tqdm import tqdm
import pandas as pd

team =[]
for tn in tqdm(range(1950, 2024)):
    url = 'https://2689web.com/' + str(tn) +'.html'
    r = requests.get(url)
    r.encoding = r.apparent_encoding
    root = html.fromstring(r.text)
    t1 = root.xpath('//*[@id="panel1"]//td[@class="nittei"]//a/@href')
    t2 = root.xpath('//*[@id="panel4"]//td[@class="nittei"]//a/@href')
    for i in range(len(t1)):
        team.append([t1[i][0:5]+t1[i][9:], 'C'])
    for i in range(len(t2)):
        team.append([t2[i][0:5]+t2[i][9:], 'P'])

print(team)

result = []
for tm in tqdm(team):
    y = tm[0][0:tm[0].find('/', 0)]
    url = 'https://2689web.com/'+ tm[0]
    r = requests.get(url)
    root = html.fromstring(r.content)
    t1 = root.xpath('//tr')
    n = t1[0].text_content()
    win = 0
    lose = 0
    for tr in t1:
        d = tr.text_content()
        if '月：' in d:
            m = int(d[0:d.find('月')])
        if '○' in d:
            if d[0:d.find('○')] =='　':
                dd = '00'
            else:
                dd = d[0:d.find('○')].zfill(2)
            win = win + 1
            win_rate = round(win/(win+lose), 4)
            result.append([y, tm[1], n, y[0:4] + '/' + str(m).zfill(2) + '/' + dd, 1, 1,0,0, win_rate, url])
        if '●' in d:
            if d[0:d.find('●')] =='　':
                dd = '00'
            else:
                dd = d[0:d.find('●')].zfill(2)
            lose = lose + 1
            win_rate = round(win/(win+lose), 4)
            result.append([y, tm[1], n, y[0:4] + '/' + str(m).zfill(2) + '/' + dd, 1, 0,1,0, win_rate, url])
        if '△' in d:
            if d[0:d.find('△')] =='　':
                dd = '00'
            else:
                dd = d[0:d.find('△')].zfill(2)
            if (win + lose) == 0:
                win_rate = 0
            else:
                win_rate = round(win/(win+lose), 4)
            result.append([y, tm[1], n, y[0:4] + '/' + str(m).zfill(2) + '/' + dd, 1, 0,0,1, win_rate, url])

df = pd.DataFrame(result, columns=['season', 'league', 'team', 'date', 'game' ,'win','lose','draw','win rate','url'])
for i in range(len(df)):
    if df.iloc[i,3][-2:] =='00':
        df.iloc[i,3] = df.iloc[i-1,3]
        df.iloc[i,4] = 2
df.to_csv('data.csv', index = False, encoding="utf_8_sig")    
