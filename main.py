# https://github.com/htkg

from vkbottle.user import User, Message
from vkbottle import TaskManager
import pandas as pd
import yaml

with open(r'settings.yaml') as config:
    settings = yaml.load(config, Loader=yaml.FullLoader)

# You have to login using your credentials. Make sure that you disabled 2FA.
# Write your login and password in settings.yaml.
user = User(login=settings['login'], password=settings['password'])

async def friends_zodiac(user_id=user.user_id):
    '''Get zodiac signs of the page friend list. Default user_id is the authorized user id.'''
    print(user_id)
    req = await user.api.users.get(user_id)
    user_name = req[0].first_name + ' ' + req[0].last_name
    req = await user.api.request('friends.get',{"user_id": user_id, "fields": 'bdate'})
    friends = [k for k in req['items']]
    rows = []
    for i in range(len(friends)):
        first_name = friends[i].get('first_name')
        last_name = friends[i].get('last_name')
        birthdate = friends[i].get('bdate')
        if birthdate != None:
            day, month, *year = birthdate.split('.')
            day = int(day)
            astro_sign = identify_zodiac(day, month)
            lst = [first_name, last_name, birthdate, astro_sign]
            rows.append(lst)
    df = createDF(rows)
    df.to_excel('{} {}.xlsx'.format(user_id, user_name))
    print('[Friend Zodiac] Success!')


async def chat_zodiac(chat_id):
    '''Get zodiac signs by chat id. Chat is the last two NUMBERS of the CHAT LINK. 
        Example: https://vk.com/im?sel=c99
        chat_id there is 99'''
    req = await user.api.request('messages.getChat',{"chat_id": chat_id,"fields": 'bdate'})
    # req = await user.api.request('messages.getConversationMembers',{"peer_id": peer_id, "fields": 'bdate'})
    friends = [k for k in req['users']]
    rows = []
    for i in range(len(friends)):
        first_name = friends[i].get('first_name')
        last_name = friends[i].get('last_name')
        birthdate = friends[i].get('bdate')
        if birthdate != None:
            day, month, *year = birthdate.split('.')
            day = int(day)
            astro_sign = identify_zodiac(day, month)
            lst = [first_name, last_name, birthdate, astro_sign]
            rows.append(lst)
    df = createDF(rows)
    df.to_excel('{} {}.xlsx'.format(chat_id, req['title']))
    print('[Chat Zodiac] Success!')

def createDF(rows, columns=['first_name', 'last_name', 'birthdate', 'astro_sign']):
    df = pd.DataFrame(rows, columns=columns)
    return df
    

def identify_zodiac(day, month):
    ''' Identify zodiac sign function '''
    if month == '12':
        astro_sign = 'Стрелец' if (day < 22) else 'Козерог'
    elif month == '1':
        astro_sign = 'Козерог' if (day < 20) else 'Водолей'
    elif month == '2':
        astro_sign = 'Водолей' if (day < 19) else 'Рыбы'
    elif month == '3':
        astro_sign = 'Рыбы' if (day < 21) else 'Овен'
    elif month == '4':
        astro_sign = 'Овен' if (day < 20) else 'Телец'
    elif month == '5':
        astro_sign = 'Телец' if (day < 21) else 'Близнецы'
    elif month == '6':
        astro_sign = 'Близнецы' if (day < 21) else 'Рак'
    elif month == '7':
        astro_sign = 'Рак' if (day < 23) else 'Лев'
    elif month == '8':
        astro_sign = 'Лев' if (day < 23) else 'Дева'
    elif month == '9':
        astro_sign = 'Дева' if (day < 23) else 'Весы'
    elif month == '10':
        astro_sign = 'Весы' if (day < 23) else 'Скорпион'
    elif month == '11':
        astro_sign = 'Скорпион' if (day < 22) else 'Стрелец'
    return astro_sign


tm = TaskManager()
tm.add_task(friends_zodiac(1)) # Change number to the user id
tm.add_task(chat_zodiac(1)) # Change number to the chat id
tm.run()