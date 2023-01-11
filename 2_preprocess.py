from tqdm import tqdm
import pandas as pd

df = pd.read_csv('data.csv', usecols=[0,1,2,3,4,8])

print(df)    

date = []

for i in tqdm(range(len(df))):
    temp = str(df.iloc[i,3]) + '_' + str(df.iloc[i,4])
    if not temp in date:
        date.append(temp)

date = sorted(date)
team = list(set(df['team'].values.tolist()))
season = list(set(df['season'].values.tolist()))

print(team)
print(len(date))

result = pd.DataFrame(columns = ['season'] + team, index=date)

for i in tqdm(range(len(df))):
    temp_date = str(df.iloc[i,3]) + '_' + str(df.iloc[i,4])
    temp_team = df.iloc[i,2]
    result[temp_team][temp_date] = df.iloc[i,5]
    result['season'][temp_date] = df.iloc[i,0]

for s in tqdm(season):
    for t in team:
        if result.loc[result['season']==s,t].sum() != 0:
            result.loc[result['season']==s,t] = round(result.loc[result['season']==s,t].astype(float).interpolate(),4)

result.index.name = 'date'
#result = result.drop('season', axis=1)
result2 = df.loc[:,['league','team']].drop_duplicates()
P = result2.loc[result2['league']=='P','team'].tolist()
C = result2.loc[result2['league']=='C','team'].tolist()
result.loc[:,['season']+P].to_csv('p_data.csv', encoding="utf_8_sig")
result.loc[:,['season']+C].to_csv('c_data.csv', encoding="utf_8_sig")