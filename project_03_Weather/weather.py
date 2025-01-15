from tkinter import *
from PIL import Image,ImageTk

import time

print("Current Time:", time.ctime())

now = time.ctime().split()
print(now)

#Year, Month, day
year = now[4]
month = now[1]
day = now[2]
clock = now[3][0:2]


def clockToBGCODE():
    c = int(clock)
    if c >= 19 or c < 6:
        return 3
    elif c < 12:
        return 0
    elif c < 17:
        return 1
    else:
        return 2


#base_date format
#ex. '20240614'

def genBaseDateCode():
    code = year
    mon2num = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
               'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    code += mon2num[month]
    code += day

    return code
    
##print('basedateCode:',genBaseDateCode())

dateCode = genBaseDateCode()

import requests
import json

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
key='Ts+NMfEsOgySQHW4+bWRkZP21N8vBTl4bqCkgyB8uzQMES9dcxmiADWp5qopwg9j0CqzjRWst+RYPI6ElYSbiA=='
params ={'serviceKey' : key, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON',
         'base_date' : dateCode, 'base_time' : '0500', 'nx' : '55', 'ny' : '127' }


response = requests.get(url, params=params)
res_json = json.loads(response.content)


items = res_json['response']['body']['items']['item']

tempInfo = {'Date':[], 'Time':[], 'Temp':[], 'SKY':[], 'POP':[], 'PCP':[], 'PTY':[]}
n = 0

for i in items:
    if i['category'] == 'TMP':
        tempInfo['Date'].append(i['fcstDate'])
        tempInfo['Temp'].append(i['fcstValue'])
        tempInfo['Time'].append(i['fcstTime'][:2]+'H')
        n += 1
    elif i['category'] == 'POP' and tempInfo['Date'][n-1] == i['fcstDate']:
        tempInfo['POP'].append(i['fcstValue'])
    elif i['category'] == 'PCP' and tempInfo['Date'][n-1] == i['fcstDate']:
        tempInfo['PCP'].append(i['fcstValue'])
    elif i['category'] == 'SKY' and tempInfo['Date'][n-1] == i['fcstDate']:
        tempInfo['SKY'].append(i['fcstValue'])
    elif i['category'] == 'PTY' and tempInfo['Date'][n-1] == i['fcstDate']:
        tempInfo['PTY'].append(i['fcstValue'])

dateChecked = [0,'0']
for i in range(n):
##    print(tempInfo['Date'][i], tempInfo['Time'][i], tempInfo['Temp'][i], tempInfo['SKY'][i], tempInfo['POP'][i], tempInfo['PCP'][i], tempInfo['PTY'][i])
    if dateChecked[0] == 0 and tempInfo['Date'][i] != dateChecked[1] and tempInfo['Time'][i] == clock+'H':  #오늘, 현재 시각
        day0 = [ tempInfo['SKY'][i], tempInfo['Temp'][i], None, tempInfo['PTY'][i], tempInfo['PCP'][i], tempInfo['POP'][i]]
        dateChecked = [1, tempInfo['Date'][i]]
    if dateChecked[0] == 1 and tempInfo['Date'][i] != dateChecked[1] and tempInfo['Time'][i] == '12H':  #내일, 정오
        day1 = [ tempInfo['SKY'][i], tempInfo['Temp'][i], None, tempInfo['PTY'][i], tempInfo['PCP'][i], tempInfo['POP'][i]]
        dateChecked = [2, tempInfo['Date'][i]]
    if dateChecked[0] == 2 and tempInfo['Date'][i] != dateChecked[1] and tempInfo['Time'][i] == '12H':  #이틀 뒤, 정오
        day2 = [ tempInfo['SKY'][i], tempInfo['Temp'][i], None, tempInfo['PTY'][i], tempInfo['PCP'][i], tempInfo['POP'][i]]
        dateChecked = [3, tempInfo['Date'][i]]


dateCode = dateCode[:4]+'-'+dateCode[4:6]+'-'+dateCode[6:]

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
key='Ts+NMfEsOgySQHW4+bWRkZP21N8vBTl4bqCkgyB8uzQMES9dcxmiADWp5qopwg9j0CqzjRWst+RYPI6ElYSbiA=='

params ={'serviceKey' : key, 'returnType' : 'JSON', 'numOfRows' : '100', 'pageNo' : '1', 'searchDate':dateCode}

response = requests.get(url, params=params)
res_json = json.loads(response.content)
items = res_json['response']['body']['items']

result = dict()
for row in items:
    raw = row['informGrade'].split(',')
    for pos in raw:
        if '인천 :' in pos and row['informCode']=='PM10':
            result[row['informData']] = pos[5:]
            break
print(result)

result = list(result.values())

day0[2] = result[0]
day1[2] = result[1]
day2[2] = '알 수 없음'

#표출 기준
#data1 - 오늘. 현재 시각의 정보를 바탕으로.
#data2 - 내일. 12시(정오) 시각의 정보를 바탕으로. (기온은 일일 평균 or 최저 ~ 최고)
#data3 - 이틀 후. 12시(정오) 시각의 정보를 바탕으로.

#데이터 순서: 맑음/흐림, 기온, 미세먼지양, 강우형태, 강우량, 강수확률
print("<<데이터 기록>>")
print("지금:",day0)
print("내일:",day1)
print("모레:",day2)







window = Tk()
window.title("Weather")
window.geometry("1200x800")
window['bg'] = '#0000D0'

#이미지 불러오기
bottomImg = Image.open('./images/airq_scale.png')  #하단 airq_scale.png
bottomImg = bottomImg.resize((1180,130))
bottomImg = ImageTk.PhotoImage(bottomImg)
airFaces = []  # verygood, good, normal, bad, terrible 순서대로 이미지를 저장
for filename in ['verygood.png', 'good.png', 'normal.png', 'bad.png', 'terrible.png']:
    img = Image.open('./images/'+filename )
    img = img.resize((110,75))
    img = ImageTk.PhotoImage(img)
    airFaces.append(img)

dataToIndex = {'아주 좋음':0, '좋음': 1, '보통':2, '나쁨':3, '매우 나쁨':4}

weatherSKY = []  # unknwon(0), sun(1), unknwon(2), cloudy(3), cloudy(4)  순으로 저장
for filename in ['sun.png','sun.png','sun.png', 'cloudy.png', 'cloudy.png']:
    img = Image.open('./images/'+filename )
    img = img.resize((110,75))
    img = ImageTk.PhotoImage(img)
    weatherSKY.append(img)
weatherPTY = []  # wind(0), rainy(1), rain/snow(2), snow(3), mist(4) 순으로 저장 
for filename in ['wind.png', 'rainy.png', 'rainy.png', 'snow.png', 'mist.png']:
    img = Image.open('./images/'+filename )
    img = img.resize((110,75))
    img = ImageTk.PhotoImage(img)
    weatherPTY.append(img)
bgImg = []  #main1, main2, main3, main4 순으로 저장
for filename in ['main1.png', 'main2.png', 'main3.png', 'main4.png']:
    img = Image.open('./images/'+filename )
    img = img.resize((1180,500))
    img = ImageTk.PhotoImage(img)
    bgImg.append(img)

umbImg = Image.open('./images/umb.png')#하단 airq_scale.png
umbImg = umbImg.resize((110,75))
umbImg = ImageTk.PhotoImage(umbImg)


dayBanner = Frame(window)
dayBanner['bg'] = '#60B0FF'
dayBanner.place(x=10,y=10,width=1180, height=130)

bottomBanner = Frame(window)
bottomBanner['bg'] = '#65F03A'
bottomBanner.place(x=10,y=660,width=1180, height=130)

mainFrame = Frame(window)
mainFrame['bg'] = '#80D0FF'
mainFrame.place(x=10,y=150,width=1180, height=500)

dayLabel = Label(dayBanner)
dayLabel['bg'] = dayBanner['bg']
dayLabel['font'] = ('배달의민족 주아', 64, 'bold')
dayLabel['text'] = month + ' ' + day + ', ' + year
dayLabel.place(x=0,y=0,width=1180,height=130)

dustLabel = Label(bottomBanner)
dustLabel['bg'] = bottomBanner['bg']
dustLabel['font'] = ('배달의민족 주아', 56, 'bold')
##dustLabel['text'] = '😀::::::::::::::::::::::::::::::::::::::::::::::😡'
dustLabel['image'] = bottomImg
dustLabel.place(x=0,y=0,width=1180,height=130)

mainCanvas = Canvas(mainFrame)
mainCanvas['bg'] = mainFrame['bg']
mainCanvas.place(x=-2,y=-2,width=1184, height=504)
mainCanvas.create_image(1184/2, 504/2, image=bgImg[clockToBGCODE()])

tags = ['clr','tmp', 'dust_face', 'dust_text', 'rain', 'rain_mm', 'umb','rain_prob']  
inits = [0]*len(tags)

dataFrame_1 = Frame(mainFrame)
dataFrame_1['highlightthickness'] = 10
dataFrame_1['highlightbackground'] = '#0000D0'
dataFrame_1['bg'] = '#EAEAEA'
dataFrame_1.place(x=100,y=80,width = 290, height=340)

data1 = dict()
for i in range(4):
    tag = tags[i*2]
    data1[tag] = Label(dataFrame_1)
    data1[tag]['text'] = inits[i*2]
    data1[tag].place(x=0,y=320/4*i,width=270/2,height=320/4)
    tag = tags[i*2+1]
    data1[tag] = Label(dataFrame_1)
    data1[tag]['text'] = inits[i*2+1]
    data1[tag].place(x=270/2,y=320/4*i,width=270/2,height=320/4)


##API 통해서 불러온 결과에 따라 이미지가 달라질수 있다.
data1['clr']['image'] = weatherSKY[int(day0[0])]
data1['tmp']['text'] = day0[1]+'˚C'
data1['dust_face']['image'] = airFaces[dataToIndex[day0[2]]]
data1['dust_text']['text'] = day0[2]
data1['rain']['image'] = weatherPTY[int(day0[3])]
data1['rain_mm']['text'] = day0[4]+'(㎜)'
data1['umb']['image'] = umbImg
data1['rain_prob']['text'] = day0[5]+'%'



dataFrame_2 = Frame(mainFrame)
dataFrame_2['highlightthickness'] = 10
dataFrame_2['highlightbackground'] = '#0000D0'
dataFrame_2['bg'] = '#EAEAEA'
dataFrame_2.place(x=450,y=80,width = 290, height=340)

data2 = dict(zip(tags,inits))
for i in range(4):
    tag = tags[i*2]
    data2[tag] = Label(dataFrame_2)
    data2[tag]['text'] = inits[i*2]
    data2[tag].place(x=0,y=320/4*i,width=270/2,height=320/4)
    tag = tags[i*2+1]
    data2[tag] = Label(dataFrame_2)
    data2[tag]['text'] = inits[i*2+1]
    data2[tag].place(x=270/2,y=320/4*i,width=270/2,height=320/4)

##API 통해서 불러온 결과에 따라 이미지가 달라질수 있다.
data2['clr']['image'] = weatherSKY[int(day1[0])]
data2['dust_face']['image'] = airFaces[dataToIndex[day1[2]]]
data2['rain']['image'] = weatherPTY[int(day1[3])]
data2['umb']['image'] = umbImg
data2['tmp']['text'] = day1[1]+'˚C'
data2['dust_text']['text'] = day1[2]
data2['rain_mm']['text'] = day1[4]+'(㎜)'
data2['rain_prob']['text'] = day1[5]+'%'


dataFrame_3 = Frame(mainFrame)
dataFrame_3['highlightthickness'] = 10
dataFrame_3['highlightbackground'] = '#0000D0'
dataFrame_3['bg'] = '#EAEAEA'
dataFrame_3.place(x=800,y=80,width = 290, height=340)

data3 = dict(zip(tags,inits))
for i in range(4):
    tag = tags[i*2]
    data3[tag] = Label(dataFrame_3)
    data3[tag]['text'] = inits[i*2]
    data3[tag].place(x=0,y=320/4*i,width=270/2,height=320/4)
    tag = tags[i*2+1]
    data3[tag] = Label(dataFrame_3)
    data3[tag]['text'] = inits[i*2+1]
    data3[tag].place(x=270/2,y=320/4*i,width=270/2,height=320/4)

##API 통해서 불러온 결과에 따라 이미지가 달라질수 있다.
data3['clr']['image'] = weatherSKY[int(day2[0])]
data3['dust_face']['image'] = airFaces[2]
data3['rain']['image'] = weatherPTY[int(day2[3])]
data3['umb']['image'] = umbImg
data3['tmp']['text'] = day2[1]+'˚C'
data3['dust_text']['text'] = day2[2]
data3['rain_mm']['text'] = day2[4]+'(㎜)'
data3['rain_prob']['text'] = day2[5]+'%'

window.mainloop()
