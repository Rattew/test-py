import requests
import datetime
import telebot

token = ''
tgb = ''

def telegram_bot(tgb):
    bot = telebot.TeleBot(tgb)
    
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет! Введи название города, чтобы узнать погоду!')
    
    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text == 'trg':
            city = 'Tryokhgorny'
        elif message.text == 'ekb':
            city = 'Yekaterinburg'
        else:
            city = message.text
        geolocation(message, city)
        
    def geolocation(message, city):
        try:
            req_geo = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={token}&lang=ru').json()
            city = req_geo[0]['local_names']['ru']
            lat = req_geo[0]['lat'] 
            lon = req_geo[0]['lon']
            get_curr_data(message, city, lat, lon)
            get_tom_data(message, lat, lon)
        except:
            bot.send_message(message.chat.id, 'Некорректный ввод')
            
    def get_curr_data(message, city, lat, lon):
        req_weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&lang=ru&units=metric').json()
        temp_min = req_weather['main']['temp_min']
        temp_max = req_weather['main']['temp_max']
        sky = req_weather['weather'][0]['description']
        humidity = req_weather['main']['humidity']
        pressure = req_weather['main']['pressure']
        wind = req_weather['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(req_weather['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(req_weather['sys']['sunset'])
        day_len = sunset - sunrise
        bot.send_message(message.chat.id, f'Погода в городе: {city}\nТемпература: {temp_min}-{temp_max} C°\n'
              f'Облачность: {sky}\nВлажность: {humidity}%\nВетер: {wind} м/c\nДавление: {pressure} мм\n'
              f'Восход: {sunrise}\nЗакат: {sunset}\nПродолжительность дня: {day_len}')
    
    def get_tom_data(message, lat, lon):
        req_weather = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={token}&lang=ru&units=metric').json()
        bot.send_message(message.chat.id, 'Прогноз на ближайшее время:')
        for i in range(2, 7, 2):
            forcast = req_weather['list'][i]
            raw_time = list(forcast['dt_txt'])
            cut_time = raw_time[11:]
            time = ''.join(cut_time)
            sky = forcast['weather'][0]['description']
            humidity = forcast['main']['humidity']
            temp = forcast['main']['temp']
            wind = forcast['wind']['speed']
            pressure = forcast['main']['pressure']
            bot.send_message(message.chat.id, f'{time}\n'
                             f'Температура: {temp} C°\n'
                             f'Облачность: {sky}\n'
                             f'Влажность: {humidity}%\n'
                             f'Ветер: {wind} м/c\n'
                             f'Давление: {pressure} мм')              
                
    bot.polling()

if __name__ == '__main__':
    telegram_bot(tgb)
