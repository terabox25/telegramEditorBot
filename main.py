# coding=utf-8

from config import TOKEN
from videoedit import *
import telebot as tb
import os
import uuid

bot = tb.TeleBot(TOKEN)

dialogues = {}

for i in ['InputFiles', 'OutputFiles']:
    if os.path.exists(i):
        pass
    else:
        os.mkdir(i)

def savevideo(message):
    video = message.video
    file_info = bot.get_file(video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'InputFiles/{message.from_user.id}.mp4', 'wb') as file:
        file.write(downloaded_file)
        file.close()

def savevideoformerging(message):
    video = message.video
    file_info = bot.get_file(video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'InputFiles/{message.from_user.id}_{str(uuid.uuid4())[:8]}.mp4', 'wb') as file:
        file.write(downloaded_file)
        file.close()

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = tb.types.InlineKeyboardMarkup([[
        tb.types.InlineKeyboardButton('Обрезать ✂️', callback_data='Cut'),
        tb.types.InlineKeyboardButton('Ускорить ⏏️', callback_data='Speed'),
        tb.types.InlineKeyboardButton('Склеить 🎞', callback_data='Concatenate')
    ]])
    bot.send_message(message.chat.id, '''Привет, я бот созданный для редактирования видеофайлов.
Выбери действие''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'Continue':
        mergevideos(call.from_user.id)
        bot.send_video(call.from_user.id, video=open(f'OutputFiles/{call.from_user.id}.mp4', 'rb'))        
        files = [file_ for file_ in os.listdir('InputFiles/') if str(call.from_user.id) in file_]
        [os.unlink('InputFiles/' + file_) for file_ in files]
        os.unlink(f'OutputFiles/{call.from_user.id}.mp4')
    else:
        dialogues[call.from_user.id] = call.data
        bot.send_message(call.from_user.id, 'Пришли мне свое видео')

@bot.message_handler(content_types=['video'])
def getuservideo(message):
    match dialogues.get(message.from_user.id):
        case 'Cut':
            print('Cut')
            try:
                savevideo(message=message)
                bot.send_message(message.chat.id, '''Хорошо, пришли мне таймкоды в таком формате:
Начальный таймкод:Конечный таймкод (Если какой-то из таймкодов больше минуты, используйте секунды:\n1 минута 30 сек. :\n90)''')
            except:
                bot.send_message(message.chat.id, "Что-то пошло не так при скачивании файла. Возможно он поврежден или его размер привышает 20МБ?")
        case 'Speed':
            try:
                savevideo(message=message)
                bot.send_message(message.chat.id, '''Во сколько раз мне ускорить видео? Пришли мне число вот в таком формате:
Число''')
            except:
                bot.send_message(message.chat.id, "Что-то пошло не так при скачивании файла. Возможно он поврежден или его размер привышает 20МБ?") 
        case 'Concatenate':
            keyboard = tb.types.InlineKeyboardMarkup([[
                tb.types.InlineKeyboardButton('Склеить', callback_data='Continue')
            ]])
            try: 
                savevideoformerging(message)
                bot.send_message(message.chat.id, 'Дальше просто присылай мне свои видео для склейки', reply_markup=keyboard)
            except:
               bot.send_message(message.chat.id, "Что-то пошло не так при скачивании файла. Возможно он поврежден или его размер привышает 20МБ?") 
 

@bot.message_handler(content_types=['text'])
def getparams(message):
    match dialogues.get(message.from_user.id):
        case 'Cut':
            try:
                from_, to = tuple(map(int, message.text.split(':')))
                cropvideo(video=VideoFileClip(f'InputFiles/{message.from_user.id}.mp4'), startingtime=from_, endingtime=to, id=message.from_user.id)
                bot.send_message(message.chat.id, 'Высылаю видео...')
                bot.send_video(message.chat.id, video=open(f'OutputFiles/{message.from_user.id}.mp4', 'rb'))
            except:
                bot.send_message(message.chat.id, "Что-то пошло не так при обработке видео :(")
        case 'Speed':
            try:
                speed = int(message.text)
                speedupvideo(video=VideoFileClip(f'InputFiles/{message.from_user.id}.mp4'), speed=speed, id=message.from_user.id)
                bot.send_message(message.chat.id, 'Высылаю видео...')
                bot.send_video(message.chat.id, video=open(f'OutputFiles/{message.from_user.id}.mp4', 'rb'))
            except:
                bot.send_message(message.chat.id, "Что-то пошло не так при обработке видео :(")

    os.remove(f'InputFiles/{message.from_user.id}.mp4')
    os.remove(f'OutputFiles/{message.from_user.id}.mp4')
    del dialogues[message.from_user.id]


bot.polling()
