import eel
import datetime
import time
import win32com.client as wincl
from pyttsx3 import voice
speak = wincl.Dispatch ( "SAPI.SpVoice" )
import speech_recognition as sr
import os
import sys
import webbrowser
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
import random
import requests
from datetime import datetime
import geocoder
from threading import Thread
from time import sleep
import pyowm
global ot
import vk_api
import math
from translate import Translator
from gtts import gTTS
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

translator=Translator(from_lang="ru", to_lang="en")

my_token = 'cb7a9d89889a68851abbf90438ced52ce4da714c70b8a96d0bd50ec6da0975dcfe69d233502aafdc88578'
session = vk_api.VkApi(token = my_token)
vk = session.get_api()

events=[]
data=[]
dela=0

birthday=str('')

not_sleep_time=str('')
not_sleep_hour=25
not_sleep_minute=61

opts = {"tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'как','сколько','поставь','переведи', "засеки",'запусти','сколько будет'),
        "cmds":
            {"stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты', "шутка", "прикол"),
             "calc": ('скажи сколько будет', 'прибавить','умножить','разделить','степень','вычесть','поделить','х','+','-','/'),
             "shutdown": ('выключи', 'выключить', 'отключение', 'отключи', 'выключи компьютер'),
             "conv": ("валюта", "конвертер","доллар", 'курс', 'руб','евро'),
             "translator": ("переводчик","translate", 'переведи')}}

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
                
    return RC

def talk(words):
    speak.Speak(words)
    os.system("say " + words)

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk("Я вас слушаю")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio, language="ru-RU").lower()
    except sr.UnknownValueError:
        talk("Я вас не понимаю, сэр")
        zadanie = command()
    return zadanie

def comanda():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio, language="ru-RU").lower()
    except sr.UnknownValueError:
        talk("Я вас не понимаю, сэр")
        zadanie = command()
    return zadanie

def start_commanda():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio, language="ru-RU").lower()
    except sr.UnknownValueError:
        zadanie = command()
    return zadanie

def send_mail(email, password, FROM, TO, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    
def call_at_interval(period, callback, args):
	while True:
		sleep(period)
		callback(*args)

def setInterval(period, callback, *args):
	Thread(target=call_at_interval, args=(period, callback, args)).start()

def pomnit(something):
    global dela
    global events
    global data
    global not_sleep_time
    global not_sleep_hour
    global not_sleep_minute
    actual_time=datetime.now()
    
    if dela>0:
        for i in range(dela):
            event_data=data[i]
            if event_data[2:3]=='0' or event_data[2:3]=='1':
                year=int(event_data[5:9])
                month=int(event_data[2:4])
                day=int(event_data[0:2])
            else:
                year=int(event_data[6:10])
                month=int(event_data[3:5])
                day=int(event_data[0:2])
            if actual_time.year>year or (actual_time.year==year and actual_time.month>month) or (actual_time.year==year and actual_time.month==month and actual_time.day>day):
                data=data[0:i]+data[i+1:]
                events=events[0:i]+events[i+1:]
                dela-=1
    if actual_time.hour==20 and actual_time.minute==00 and actual_time.second<31:
        for i in range(dela):
            event_data=data[i]
            if event_data[2:3]=='0' or event_data[2:3]=='1':
                year=int(event_data[5:9])
                month=int(event_data[2:4])
                day=int(event_data[0:2])
            else:
                year=int(event_data[6:10])
                month=int(event_data[3:5])
                day=int(event_data[0:2])
            if day>7:
                if year==actual_time.year and month==actual_time.month and day<=actual_time.day+7:
                    talk("сэр, у вас менее чем через неделю важное событие, сейчас уточню")
                    talk(events[i])
                    talk("запланированно на")
                    talk(day)
                    talk(month)
                    talk(year)
            else:
                if month==1:
                    if (year==actual_time.year) or (year==actual_time.year+1 and actual_time.month==12 and day+30<=actual_time.day+7):
                        talk("сэр, у вас менее чем через неделю важное событие, сейчас уточню")
                        talk(events[i])
                        talk("запланированно на")
                        talk(day)
                        talk(month)
                        talk(year)
                else:
                    if (year==actual_time.year and month==actual_time.month) or (year==actual_time.year and actual_time.month+1==month and day+30<=actual_time.day+7):
                        talk("сэр, у вас менее чем через неделю важное событие, сейчас уточню")
                        talk(events[i])
                        talk("запланированно на")
                        talk(day)
                        talk(month)
                        talk(year)
                        
    if actual_time.hour==int(not_sleep_hour) and actual_time.minute==int(not_sleep_minute):
        talk("сэр, сейчас")
        talk(not_sleep_hour)
        talk(not_sleep_minute)
        os.startfile(r'будильник.mp3')
        not_sleep_time=str()
        not_sleep_hour=25
        not_sleep_minute=61
setInterval(30, pomnit, 1)



def browser():
    sites = {"https://vk.com":["vk","вк"], 'https://www.youtube.com/':['youtube', 'ютуб'], 'https://ru.wikipedia.org': ["вики", "wiki"], 'http://google.com':['гугл','google']}
    site = voice.split()[-1]
    for k, v in sites.items():
        for i in v:
            if i not in site.lower():
                open_tab = None
            else:
                open_tab = webbrowser.open_new_tab(k)
                break

        if open_tab is not None:
            break

def getanswer(text):
    try:
        text = text.lower().strip()
        if os.path.exists('boltun.txt'):
            a = 0
            n = 0
            nn = 0
            file = open('boltun.txt', 'r', encoding='utf-8')
            mas = file.read().split('\n')

            for q in mas:
                if ('u: ' in q):
                    aa = (fuzz.token_sort_ratio(q.replace('u: ', ''), text))
                    if (aa > a and aa != a):
                        a = aa
                        nn = n
                n = n + 1
            s = mas[nn + 1]
            return s
        else:
            return 'Нет ответа'
    except:
        return 'Нет ответа'

def myvopros(data):
    ot = getanswer(data)
    return(ot)

def makeSomething(zadanie):
    if 'открой вконтакте' in zadanie:
        talk("Уже открываю")
        url1 = 'https://vk.com/audios389122209'
        webbrowser.open(url1)
    elif 'поставь будильник' in zadanie:
        talk("на какое время?")
        global not_sleep_time
        global not_sleep_hour
        global not_sleep_minute
        not_sleep_time=comanda()
        if not_sleep_time[1]==str(' ') or not_sleep_time[1]==str(':'):
            not_sleep_hour=not_sleep_time[0]
            not_sleep_minute=not_sleep_time[2:4]
        elif not_sleep_time[2]==str(' '):
            not_sleep_hour=not_sleep_time[0:2]
            not_sleep_minute=not_sleep_time[3:5]
        else:
            not_sleep_hour=not_sleep_time[0:2]
            not_sleep_minute=not_sleep_time[2:4]
        if not_sleep_minute[0]=='0':
            not_sleep_minute=not_sleep_minute[1]
        talk("готово")
    elif 'долго ехать до школы' in zadanie:
        url='https://yandex.ru/maps/65/novosibirsk/?l=trf%2Ctrfe&ll=83.080895%2C54.849630&mode=routes&rtd=0&rtext=54.855396%2C83.049373~54.842927%2C83.106371&rtt=auto&ruri=~ymapsbm1%3A%2F%2Forg%3Foid%3D1207856774&z=14.52'
        a=requests.get(url)
        b=BeautifulSoup(a.content, 'html.parser')
        c=b.find(class_="auto-route-snippet-view__route-title-primary")
        talk(str(c)[58:60])
        talk('минут')
    elif 'дополни список дел' in zadanie:
        talk("скажите всё когда закончите")
        new_event=str("")
        while(new_event!=str('всё')):
            global dela
            global data
            global events
            new_event=command()
            events.append(new_event)
            talk("какого числа это будет?")
            new_event_date=str(comanda())
            data.append(new_event_date)
            dela+=1
        dela-=1
        events=events[:-1]
        data=data[:-1]
    elif 'перечисли дела' in zadanie:
        if dela>0:
            for i in range(dela):
                talk(events[i])
                talk("запланированно на")
                it_event_date=data[i]
                if it_event_date[2:3]=='0' or it_event_date[2:3]=='1':
                    talk(it_event_date[0:2])
                    talk(it_event_date[2:4])
                    talk(it_event_date[5:9])
                else:
                    talk(it_event_date[0:2])
                    talk(it_event_date[3:5])
                    talk(it_event_date[6:10])
        else:
            talk("У вас нет запланированных дел")
    elif 'открой youtube' in zadanie:
        talk("Уже открываю")
        urly = 'https://www.youtube.com/'
        webbrowser.open(urly)
    elif 'загугли' in zadanie:
        talk("конечно")
        a12=command()
        b12 = a12.replace(' ', '+')
        url11 = 'https://www.google.com/search?q=привет&oq=привет&aqs=chrome.0.69i59j46i433j0i20i263i433j46i20i263i433j0i433j46i433l2j0i131i433j0i433j46i433.1267j0j7&sourceid=chrome&ie=UTF-8'
        url12 = url11[0:32] + b12 + url11[38:42] + b12 + '&aqs=chrome.0.69i59j46i433j0i20i263i433j46i20i263i433j0i433j46i433l2j0i131i433j0i433j46i433.1267j0j7&sourceid=chrome&ie=UTF-8'
        webbrowser.open(url12)
    elif 'расскажи анекдот' in zadanie:
        joke = ['Заходят два дракона в бар. Один говорит другому: Что-то здесь жарковато. А тот отвечает: Рот закрой.', 'Купил мужчина шляпу, а она ему как раз.', 'Лондон. Утро. Старый английский лорд завтракает. Вбегает дворецкий и кричит: Сэр! Темза вышла из берегов!!! Лорд флегматично: Джон, выйдите, потом зайдите и доложите как следует. Дворецкий выходит, потом снова вбегает и кричит: Сэр! Темза уже у нашего дома!!! Джон, выйдите, потом зайдите и доложите как следует. Дворецкий выходит. Открывается дверь, степенно входит дворецкий, за ним в комнату врываются потоки воды:Темза, сэр!']
        number=random.randint(0, 3)
        talk(str(joke[number]))
    elif 'какая погода' in zadanie:
        r1 = geocoder.ip('me')
        city = r1.city+str(', ')+r1.country
        owm=pyowm.OWM("0fcf9348926d707519ccfa9ac0f951a9")
        mgr=owm.weather_manager()
        observation=mgr.weather_at_place(city)
        w=observation.weather
        temp=str(w.temperature('celsius')['temp'])
        minus=0
        pogoda=0
        if temp[0]=='-':
            talk("минус")
            minus=1
        if temp[minus+1]=='.':
            talk(temp[minus])
        else:
            talk(temp[minus:minus+2])
            pogoda=1
        if minus==0:
            if pogoda==0:
                talk("сегодня прохладно")
            else:
                if int(temp[0:2])<21:
                    talk("сегодня не жарко")
                else:
                    talk("сегодня жарко")
        else:
            talk("сегодня холодно")
        if w.status=='Snow':
            talk("идёт снег")
        elif w.status=='Rain':
            talk("идёт дождь, советую взять зонтик")
    elif 'прощай' in zadanie:
        talk("ещё увидимся, сэр")
        sys.exit()
    elif 'кто ты' in zadanie:
        talk("Меня зовут Джарвис, я ваш голосовой ассистент, можете обращаться ко мне с различными вопросами")
    elif 'помоги выбрать' in zadanie:
        talk('Конечно, сэр')
        y = random.randint(1, 2)
        if y == 1:
            talk('Я считаю, что первый вариант лучше')
        else:
            talk('Я считаю, что второй вариант лучше')
    elif 'я красивый' in zadanie:
        talk('сэр, вы прекрасны')
    elif 'какое сегодня число' in zadanie:
        l = datetime.now()
        l1 = l.month
        l2 = str(l.day)
        if l2==str('1'):
            talk('первое')
        elif l2==str('2'):
            talk('второе')
        elif l2==str('3'):
            talk('третье')
        elif l2==str('4'):
            talk('четвёртое')
        elif l2==str('5'):
            talk('пятое')
        elif l2==str('6'):
            talk('шестое')
        elif l2==str('7'):
            talk('седьмое')
        elif l2==str('8'):
            talk('восьмое')
        elif l2==str('9'):
            talk('девятое')
        elif l2==str('10'):
            talk('десятое')
        elif l2==str('11'):
            talk('одиннадцатое')
        elif l2==str('12'):
            talk('двенадцатое')
        elif l2==str('13'):
            talk('тринадцатое')
        elif l2==str('14'):
            talk('четырнадцатое')
        elif l2==str('15'):
            talk('пятнадцатое')
        elif l2==str('16'):
            talk('шестнадцатое')
        elif l2==str('17'):
            talk('семнадцатое')
        elif l2==str('18'):
            talk('восемнадцатое')
        elif l2==str('19'):
            talk('девятнадцатое')
        elif l2==str('20'):
            talk('двадцатое')
        elif l2==str('21'):
            talk('двадцать первое')
        elif l2==str('22'):
            talk('двадцать второе')
        elif l2==str('23'):
            talk('двадцать третье')
        elif l2==str('24'):
            talk('двадцать четвертое')
        elif l2==str('25'):
            talk('двадцать пятое')
        elif l2==str('26'):
            talk('двадцать шестое')
        elif l2==str('27'):
            talk('двадцать седьмое')
        elif l2==str('28'):
            talk('двадцать восьмое')
        elif l2==str('29'):
            talk('двадцать девятое')
        elif l2==str('30'):
            talk('тридцатое')
        elif l2==str('31'):
            talk('тридцать первое')

        if l1==1:
            talk('января')
        elif l1==2:
            talk('февраля')
        elif l1==3:
            talk('марта')
        elif l1==4:
            talk('апреля')
        elif l1==5:
            talk('мая')
        elif l1==6:
            talk('июня')
        elif l1==7:
            talk('июля')
        elif l1==8:
            talk('августа')
        elif l1==9:
            talk('сентября')
        elif l1==10:
            talk('октября')
        elif l1==11:
            talk('ноября')
        elif l1==12:
            talk('декабря')
    elif 'который час' in zadanie:
        l = datetime.now()
        l4 = str(l.hour)
        l8 = int(l4)
        l5 = str(l.minute)
        l6 = int(l5)
        if l6 > 9:
            l7 = l5
        else:
            l7 = str('0') + l5
        if l8 == 0:
            l9 = str('0') + l4
        else:
            l9 = l4
        talk(l9)
        talk(l7)
    elif 'сколько дней до дня рождения' in zadanie:
        if birthday==str(''):
            talk("сэр, когда у вас день рождения?")
            birthday=comanda()
        l = datetime.now()
        x1 = datetime.now().date()
        y1 = str(x1)
        h1 = y1[5:10]
        base_date = h1
        data = ['11-19']
        format = "%m-%d"
        base = datetime.strptime(base_date, format)
        diff = [(datetime.strptime(d, format) - base).days for d in data]
        c1 = [0]
        b1 = l.year
        if diff > c1 or diff == c1:
            v1 = diff
        else:
            if b1 == 3:
                v1 = diff + 366
            else:
                v1 = diff + 365
        v1 = str(v1)
        if v1 == 0:
            talk(v1)
            talk('С днём рождения, сэр!')
        else:
            talk(v1)
    elif 'открой компас' in zadanie:
        talk('конечно, сэр')
        os.startfile(r'C:\Program Files\ASCON\KOMPAS-3D v18 Study\Bin\kStudy.Exe')
    elif 'открой презентации' in zadanie:
        talk('конечно, сэр')
        os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE')
    elif 'открой word' in zadanie:
        talk('конечно, сэр')
        os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE')
    elif 'открой гейб' in zadanie:
        talk('конечно, сэр')
        os.startfile(r'C:\Program Files\GIMP 2\bin\gimp-2.10.exe')
    elif 'открой иксель' in zadanie:
        talk('конечно, сэр')
        os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE')
    elif 'открой калькулятор' in zadanie:
        talk('конечно, сэр')
        calc=command()
        i=0
        first=0
        while i!=-1:
            if calc[i]==str(' '):
                first=i
                i=-1
            else:
                i+=1
        second=0
        j=first+2
        while j!=-1:
            if calc[j]==str(' '):
                second=j
                j=-1
            else:
                j+=1
        first_operand=int(calc[:first])
        second_operand=int(calc[second+1:])
        operation=calc[first+1:second]
        if operation==str('+'):
            result=first_operand+second_operand
        elif operation==str('-'):
            result=first_operand-second_operand
        elif operation==str('*'):
            result=first_operand*second_operand
        elif operation==str('/'):
            result=first_operand/second_operand
        elif operation==str('логарифм'):
            result=math.log(second_operand, first_operand)
        elif operation==str('степень'):
            result=first_operand**second_operand
        elif operation==str('корень'):
            result=second_operand**(1/first_operand)
        elif operation==str('синус'):
            if first_operand==1:
                result=math.sin(math.radians(second_operand))
            else:
                result=math.sin(second_operand)
        elif operation==str('косинус'):
            if first_operand==1:
                result=math.cos(math.radians(second_operand))
            else:
                result=math.cos(second_operand)
        elif operation==str('тангенс'):
            if first_operand==1:
                result=math.tan(math.radians(second_operand))
            else:
                result=math.tan(second_operand)
        talk(str(result))
    elif 'открой переводчик' in zadanie:
        text=command()
        result=translator.translate(text)
        myobj=gTTS(text=result, lang='en', slow=False)
        myobj.save("text.mp3")
        os.system("text.mp3")
    elif 'открой курс валют' in zadanie:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        talk('курс доллара')
        talk(str(round(data['Valute']['USD']['Value'])))
        talk('курс евро')
        talk(str(round(data['Valute']['EUR']['Value'])))
    elif 'отправь письмо' in zadanie:
        talk('введите данные и нажмите отправить')
    elif 'давай поговорим' in zadanie:
        talk('на какую тему?')
        tema=comanda()
        talk('расскажите что нибудь интересное')
        something=comanda()
        talk('круто, мне порнавилось')
    


@eel.expose
def call_in_js(xyz):
    while True:
        makeSomething(start_commanda())

@eel.expose
def last_stop(y):
    sys.exit()

@eel.expose
def send(login, passwords, TO):
    email=login
    password='Fsr282373'
    FROM=login
    talk('скажите тему письма')
    subject=comanda()
    msg = MIMEMultipart("alternative")
    msg["From"] = FROM
    msg["To"] = TO
    msg["Subject"] = subject
    talk('скажите текст письма')
    html = comanda()
    text = BeautifulSoup(html, "html.parser").text
    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")
    msg.attach(text_part)
    msg.attach(html_part)
    try:
        send_mail(email, password, FROM, TO, msg)
        talk('ваше письмо отправлено')
    except:
        talk('к сожалению, мне не удалось отправить письмо, проверьте введённые логин и пароль')

eel.init("web")
eel.start("main1.html", size=(700, 750))
