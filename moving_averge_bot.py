

pip install yahoofinancials
pip install yfinance
pip install pytelegrambotapi

import pandas as pd
import yfinance as yf
import yahoofinancials
import numpy as np
import time
import requests
import telebot

#функция, отправляющая сообщение пользователю 
def send_telegram(text: str):
    token = "your token"
    url = "https://api.telegram.org/bot"
    bot_id = "id бота или канала, в котором есть бот"  
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": bot_id,
         "text": text,
          })

    if r.status_code != 200:
        raise Exception("post_text error")

bot = telebot.TeleBot('your token')

def signal_response(ticker): 
  buyer = 0
  #импортим данные 
  data = yf.download('{}'.format(ticker), start ='start data',interval='1m',progress=False)


  # Добавим short & long moving averages 
  data['MA10'] = data['Close'].rolling(10).mean()
  data['MA100'] = data['Close'].rolling(100).mean()
  data = data.dropna()

  #сигналы: 1 - покупка, 0 - продажа 
  data['Signals'] = [1 if data.loc[i, 'MA10'] < data.loc[i, 'MA100'] else 0 for i in data.index] 

    
  if data['Signals'][-1] == 1:
    if buyer == 0:
      # проверка того, достигнуто ли дно (если цена поднялась, значит дно достигнуто и пройдено(правда могут быть и локальные "просадки"))
      if data['Close'][-1] > data['Close'][-2]: 
        msg = 'BUY signal! Current price {}'.format(data['Close'][-1])
        send_telegram(msg)
        buyer = 1
      

  if data['Signals'][-1] == 0:
    if buyer == 1:
      # проверка того, достигнут ли пик (если цена упала, значит пик достигнут и пройден(проблема с локальными пиками все еще актуальна))
      if data['Close'][-1] < data['Close'][-2]: 
        msg = 'SELL signal! Current price {}'.format(data['Close'][-1]) 
        send_telegram(msg)
        buyer = 0

# Метод, который получает сообщения и обрабатывает их 
@bot.message_handler(content_types=['text']) 
# Функция, получающая тикер от пользователя и применяющая к нему стратегию 
def get_ticker(message):
    global ticker 
    ticker = message.text.upper()  
    bot.send_message(message.from_user.id, 'Starting to analyze {}'.format(ticker))

    signal_response(ticker) 

bot.polling(none_stop=True, interval=0)
