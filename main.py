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
        tb.types.InlineKeyboardButton('Cut ✂️', callback_data='Cut'),
        tb.types.InlineKeyboardButton('Speed Up ⏏️', callback_data='Speed'),
        tb.types.InlineKeyboardButton('Merge 🎞', callback_data='Concatenate')
    ]])
    bot.send_message(message.chat.id, '''Hello, I am a bot created for video editing.
Please select an action''', reply_markup=keyboard)

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
        bot.send_message(call.from_user.id, 'Please send me your video')

@bot.message_handler(content_types=['video'])
def getuservideo(message):
    match dialogues.get(message.from_user.id):
        case 'Cut':
            print('Cut')
            try:
                savevideo(message=message)
                bot.send_message(message.chat.id, '''Great, now send me the timecodes in this format:
Start Timecode:End Timecode (If any of the timecodes exceed one minute, use seconds:\n1 minute 30 sec. :\n90)''')
            except:
                bot.send_message(message.chat.id, "Something went wrong while downloading the file. Maybe it is corrupted or exceeds 20MB?")
        case 'Speed':
            try:
                savevideo(message=message)
                bot.send_message(message.chat.id, '''How much faster should I speed up the video? Send me the number in this format:
Number''')
            except:
                bot.send_message(message.chat.id, "Something went wrong while downloading the file. Maybe it is corrupted or exceeds 20MB?") 
        case 'Concatenate':
            keyboard = tb.types.InlineKeyboardMarkup([[
                tb.types.InlineKeyboardButton('Merge', callback_data='Continue')
            ]])
            try: 
                savevideoformerging(message)
                bot.send_message(message.chat.id, 'Now just send me your videos for merging', reply_markup=keyboard)
            except:
               bot.send_message(message.chat.id, "Something went wrong while downloading the file. Maybe it is corrupted or exceeds 20MB?") 
 

@bot.message_handler(content_types=['text'])
def getparams(message):
    match dialogues.get(message.from_user.id):
        case 'Cut':
            try:
                from_, to = tuple(map(int, message.text.split(':')))
                cropvideo(video=VideoFileClip(f'InputFiles/{message.from_user.id}.mp4'), startingtime=from_, endingtime=to, id=message.from_user.id)
                bot.send_message(message.chat.id, 'Sending you the video...')
                bot.send_video(message.chat.id, video=open(f'OutputFiles/{message.from_user.id}.mp4', 'rb'))
            except:
                bot.send_message(message.chat.id, "Something went wrong while processing the video :(")
        case 'Speed':
            try:
                speed = int(message.text)
                speedupvideo(video=VideoFileClip(f'InputFiles/{message.from_user.id}.mp4'), speed=speed, id=message.from_user.id)
                bot.send_message(message.chat.id, 'Sending you the video...')
                bot.send_video(message.chat.id, video=open(f'OutputFiles/{message.from_user.id}.mp4', 'rb'))
            except:
                bot.send_message(message.chat.id, "Something went wrong while processing the video :(")

    os.remove(f'InputFiles/{message.from_user.id}.mp4')
    os.remove(f'OutputFiles/{message.from_user.id}.mp4')
    del dialogues[message.from_user.id]

bot.polling()
