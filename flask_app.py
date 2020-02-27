from flask import Flask
from payday_counter import count

app = Flask('__name__')

@app.route('/')
def index():
    return 'Index Page'

@app.route('/payday/<int:num>')
def payday(num):
    return f'<p align=center>다음 월급까지 남은 날!!!<br>{count(num)}</p>'



''' legacy below
# from flask import Flask, render_template, request
# from datetime import datetime
# from faker import Faker

# app = Flask(__name__)
# fake = Faker()
# # fake = Faker(ko_Kr)

# @app.route('/')
# def home():
#     return 'happy hacking!'

# @app.route('/ssafy')
# def ssafy():
#     return 'This is SSAFY'

# @app.route('/hello/<name>')
# def hello(name):
#     return f'Hello {name}'

# # /cube/1 => 1
# # /cube/2 => 8
# # /cube/3 => 27
# @app.route('/cube/<int:num>')
# def cube(num):
#     return str(num ** 3)

# # datetime
# @app.route('/newyear')
# def newyear():
#     if datetime.month == 1 and datetime.day == 1:
#         return '네'
#     else:
#         return '아니요'

# @app.route('/html')
# def html():
#     return render_template('home.html')

# @app.route('/pastlife')
# def pastlife():
#     return render_template('pastlife.html')

# @app.route('/result')
# def result():
#     userName = request.args.get('userName')    # pastlife/로부터 넘겨진 사용자의 이름을 받아온다.
#     job = fake.job()
#     return render_template('result.html', userName = userName, job = job)

from flask import Flask, render_template, request
import requests
from pprint import pprint
import random
from decouple import config

app = Flask(__name__)

base_url = 'https://api.telegram.org'
client_id = config('NAVER_CLIENT_ID')
client_secret = config('NAVER_CLIENT_SECRET')
key = config('TELEGRAM_BOT_TOKEN')
update_url = f'{base_url}/bot{key}/getUpdates'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/send')
def send():
    response = requests.get(update_url).json()
    chat_id = response['result'][0]['message']['chat']['id']  # 이거 아이디설정해줘야한다. 그리고 .env에 저장해줘야한다. # config('TELEGRAM_CHAT_ID')
    text = request.args.get('msg')
    message_url = f'{base_url}/bot{key}/sendMessage?chat_id={chat_id}&text={text}'
    requests.get(message_url)
    return '메시지를 전송하였습니다.'

@app.route('/telegram', methods=['POST'])
def telegram():
    response = request.get_json()
    pprint(response)
    text = response.get('message').get('text')

    if text == '점심메뉴':
        menu = ['스테이크', '참치회', '장어곰탕', '치킨', '햄버거']
        text = random.choice(menu)
    # 로또번호 추천 봇 : '로또'
    elif text == '로또':
        text = sorted(random.sample(range(1,46), 6))
    elif text[0:4] == '/번역 ':
        # 1. papago를 통해 번역을 요청해서 받아오기
        papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
        headers = { 'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret, }
        data = { 'source': 'ko', 'target': 'en', 'text': text[4:], }
        papago_response = requests.post(papago_url, headers=headers, data=data).json()
        # 2. 받아온 결과를 telegram 메세지로 보내기
        text = papago_response.get('message').get('result').get('translatedText')
        chat_id = response.get('message').get('chat').get('id')
    message_url = f'{base_url}/bot{key}/sendMessage?chat_id={chat_id}&text={text}'
    requests.get(message_url)
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)
'''