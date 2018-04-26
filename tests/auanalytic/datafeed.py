import pandas as pd
import requests
import random

def create_data_set(user_count, componenet_count):
    df = pd.DataFrame()
    usernames = []
    points = [[] for x in xrange(componenet_count)]
    for i in range(1,user_count):
        usernames.append('user'+str(i))
        for column in points:
            clicks = random.randint(0,20)
            mouseover = clicks * random.randint(100*clicks,5000)
            column.append([clicks,mouseover])
    df['user name'] = pd.Series(usernames)
    for column in points:
        df['comp_'+ str(points.index(column) + 1) + '_clicks'] = pd.Series([item[0] for item in column])
        df['comp_'+ str(points.index(column) + 1) + '_mouseover'] = pd.Series([item[1] for item in column])
    return df
        
def save_df(df,file_name):
    df.to_csv(file_name, sep=',', encoding='utf-8')

def feed_data(url,file_name):
    headers = {
    'Content-Type': "application/json"
    }
    df = pd.read_csv(file_name)
    for row in df.iterrows():
        index, data = row
        row_data = data.tolist()[1:]
        
        for i in range(1,len(row_data),2):

            payload = "{\"username\" : \""+row_data[0]+"\",\n\"component\" : \"comp"+str((i/2) + 1)+"\",\n\"url\" : \""+url+"\",\n\"clicks\" : "+str(row_data[i])+",\n\"mouseover\" : "+str(row_data[i+1])+"\n}"
            response = requests.request("POST","https://auanalytic.herokuapp.com/api/save" , data=payload,headers = headers)
            print(response)


'''
url = "https://auanalytic.herokuapp.com/api/save"

payload = "{\"username\" : \"user1\",\n\"component\" : \"comp2\",\n\"url\" : \"url1\",\n\"clicks\" : 6,\n\"mouseover\" : 1203\n}"
headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "b69da1a2-f666-428b-be4f-bc01a8017848"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

'''
