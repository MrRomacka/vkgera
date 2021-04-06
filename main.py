import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from googletrans import Translator
import requests
import wikipedia

class QuakeReq():
    def __init__(self, name):
        qc_req = requests.get(f'https://quake-stats.bethesda.net/api/v2/Player/Stats?name={name}')
        if qc_req.status_code == 500:
            self.status_code = 500
        else:
            self.status_code = 200
            self.name = qc_req.json()['name']

            self.duel = qc_req.json()["playerRatings"]["duel"]
            self.duel_rating = self.duel['rating']
            self.duel_deviation = self.duel["deviation"]
            self.duel_gamescount = self.duel["gamesCount"]
            self.duel_last_update = self.duel['lastChange']

            self.tdm = qc_req.json()["playerRatings"]["tdm"]
            self.tdm_rating = self.tdm['rating']
            self.tdm_deviation = self.tdm["deviation"]
            self.tdm_gamescount = self.tdm["gamesCount"]
            self.tdm_last_update = self.tdm['lastChange']

    def full_info(self):
        if self.status_code == 500:
            print('Invalid nickname, try another one')
        else:
            return (f'Name: {self.name}\n \n'
                    f'Duel: {self.duel_rating}±{self.duel_deviation} (Games: {self.duel_gamescount})\n'
                    f'2v2 TDM: {self.tdm_rating}±{self.duel_deviation} (Games: {self.tdm_gamescount})')


class WeatherReq():
    def __init__(self, city):
        self.API = 'Nah... Try your one'
        self.req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API}')

    def m_info(self):
        if self.req.status_code == 500:
            return 'Wrong city name or something else'
        else:
            wth = self.req.json()
            print(wth)
            return (f'{wth["name"]}, {wth["sys"]["country"]}: ' \
                    f'{wth["main"]["temp"]}*F, {wth["weather"][0]["main"]}')


def main():
    vk_session = vk_api.VkApi(token='Sorry, but...')
    longpoll = VkBotLongPoll(vk_session, 202300581)

    for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'].lower() == '!help':
                    mes = '''List of commands:
*!help* - command list
*!qcs {name}* - general stats from Quake Champions
*!wth {city}* - current weather
*!trans/!text* - translation from {src} to {dest}
*!change* - changing source/destination pair
*!set_timer {time in hours} hours {time in minutes} minutes* - setting timer
*!wikipage {title}* - showing first in search Wikipedia page
*!wikilang {lang}* - changing Wikipedia language
            \nOther funcs may be in dev
                '''
                    vk = vk_session.get_api()
                    if event.from_user:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                        message=mes,
                                        random_id=random.randint(0, 2 ** 64))
                    elif event.from_chat:
                        vk.messages.send(chat_id=event.chat_id,
                                         message=mes,
                                         random_id=random.randint(0, 2 ** 64))
                if event.obj.message['text'].startswith('!trans'):
                    needtotr = event.obj.message['text'][6:]
                    translator = Translator()
                    translated_one = translator.translate(needtotr, dest='ru').text
                    vk = vk_session.get_api()
                    if event.from_user:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                        message=translated_one,
                                        random_id=random.randint(0, 2 ** 64))
                    elif event.from_chat:
                        vk.messages.send(chat_id=event.chat_id,
                                         message=translated_one,
                                         random_id=random.randint(0, 2 ** 64))
                if event.obj.message['text'].startswith('!qcs'):
                    name = event.obj.message['text'].split()[1]
                    print(name)
                    qcreq = QuakeReq(name)
                    qcinf = qcreq.full_info()
                    vk = vk_session.get_api()
                    if event.from_user:
                        us_id = event.obj.message['from_id']
                        vk.messages.send(user_id=us_id,
                                        message=qcinf,
                                        random_id=random.randint(0, 2 ** 64))
                    elif event.from_chat:
                        vk.messages.send(chat_id=event.chat_id,
                                         message=qcinf,
                                         random_id=random.randint(0, 2 ** 64))
                if event.obj.message['text'].startswith('!wth'):
                    wth = WeatherReq(event.obj.message['text'][5:])
                    wthinf = wth.m_info()
                    vk = vk_session.get_api()
                    if event.from_user:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                        message=wthinf,
                                        random_id=random.randint(0, 2 ** 64))
                    elif event.from_chat:
                        vk.messages.send(chat_id=event.chat_id,
                                         message=wthinf,
                                         random_id=random.randint(0, 2 ** 64))
                if event.obj.message['text'].startswith('!wiki'):
                    vk = vk_session.get_api()
                    wikipedia.set_lang('ru')
                    pg = wikipedia.page(wikipedia.search(event.obj.message['text'][6:])[0])
                    wkinf = f'{pg.title}\n{pg.content[:400]}\n\n{pg.url}'
                    if event.from_user:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                        message=wkinf,
                                        random_id=random.randint(0, 2 ** 64))
                    elif event.from_chat:
                        vk.messages.send(chat_id=event.chat_id,
                                         message=wkinf,
                                         random_id=random.randint(0, 2 ** 64))

if __name__ == '__main__':
    main()
