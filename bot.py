import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_markdown
import time
import os

random_num = random.randrange(1,101)
num_count = 0
num_round = 0
num_whose_chance = 0

TOKEN = os.environ.get("TOKEN")
PORT = int(os.environ.get('PORT', 5000))

updater = Updater(TOKEN)
group_lst = []
num_GROUP = ""
num_username_lst = []
num_chatid_lst = []
num_name_lst = []
num_whose_chance = 0
num_user_num = 0
num_round = 1
num_user_lst = []
num_game_started = False
num_start_time = 0
num_end_time = 0
user_point_dic = {}
number = 0
#print(n)
##while 1:
##    x = int(input())
##    if x == n:
##        print("Correct!")
##        break
##    if count == 0:
##        lie = random.randrange(2)
##        if lie == 0:
##            if x>n:
##                print("Greater than cpu number")
##            else:
##                print("Lesser than cpu number")
##        else:
##            if x<n:
##                print("Greater than cpu number")
##            else:
##                print("Lesser than cpu number")
##        count = 1
##    else:
##        count = 0
##        if x<n:
##            print("Lesser than cpu number")
##        else:
##            print("Greater than cpu number")
def end_num_game(bot,update):
    global group_lst,num_GROUP,num_username_lst,num_chatid_lst,num_name_lst,num_whose_chance,num_user_num,num_round,num_user_lst,num_game_started,num_start_time,num_end_time,user_point_dic,number
    bot.sendMessage(num_GROUP,"Game ENDED!!!")
    group_lst = []
    num_GROUP = ""
    num_username_lst = []
    num_chatid_lst = []
    num_name_lst = []
    num_whose_chance = 0
    num_user_num = 0
    num_round = 1
    num_user_lst = []
    num_game_started = False
    num_start_time = 0
    num_end_time = 0
    user_point_dic = {}
    number = 0

def join_num_game(bot,update):
    username = update.message.from_user.username
    name = update.message.from_user.first_name
    chat_id = update.message.from_user.id
    if group_lst != []:
        if chat_id not in num_chatid_lst:
            num_user_lst.append(f"{name}:{username}:{chat_id}")
            num_username_lst.append(username)
            num_chatid_lst.append(chat_id)
            num_name_lst.append(name)
            user_point_dic[chat_id] = 0
            bot.sendMessage(num_GROUP,text=f"{mention_markdown(chat_id,name)} joined the game, there are currently {len(num_user_lst)} players.",parse_mode="Markdown")

        else:
            update.message.reply_text("You have already joined the game")
    else:
        update.message.reply_text("No running game in this group.")


def get_num_from_user(bot,update):
    global num_count, number
    chat_id = update.message.from_user.id
    name = update.message.from_user.first_name
    if num_whose_chance == chat_id:
        message = update.message.text
        message = message.replace("/n ","").strip()
        #try:
        message = int(message)
        if message == number:
            bot.sendMessage(num_GROUP,"Correct! You won!!!.")
            end_num_game(bot,update)
            
        elif num_count == 0:
            lie = random.randrange(2)
            if lie == 0:
                if message > number:
                    bot.sendMessage(num_GROUP,"Your guessed number is GREATER than actual number")
                else:
                    bot.sendMessage(num_GROUP,"Your guessed number is SMALLER than actual number")
            else:
                if message < number:
                    bot.sendMessage(num_GROUP,"Your guessed number is GREATER than actual number")
                else:
                    bot.sendMessage(num_GROUP,"Your guessed number is SMALLER than actual number")
            num_count = 1
        else:
            num_count = 0
            if message < number:
                bot.sendMessage(num_GROUP,"Your guessed number is SMALLER than actual number")
            else:
                bot.sendMessage(num_GROUP,"Your guessed number is GREATER than actual number")

        num_increment(bot,update)

##        except Exception as e:
##            print(e)
##            update.message.reply_text("Not a number, please reply again")


def num_increment(bot,update):
    global num_round, number, num_whose_chance
    
    print(number)
    chat_id = num_chatid_lst[num_round]
    num_whose_chance = chat_id 
    name = num_name_lst[num_round]
    num_round += 1
    if num_round > len(num_chatid_lst)-1:
        num_round = 0 
    bot.sendMessage(num_GROUP,f"""{mention_markdown(chat_id,name+"'s")} chance\nMessage like this - /n NUMBER""",parse_mode="Markdown")

    
def start_num_game(bot,update):
    global num_game_started, number
    total_players = len(num_user_lst)

    if not num_game_started:
    
        if total_players > 1:
            bot.sendMessage(num_GROUP,f"Starting a game with {total_players} players")
            num_game_started = True
            number = random.randint(1,100)
            num_increment(bot=bot,update=update)

        else:
             update.message.reply_text("Game must have atleast 2 players.")

    else:
        update.message.reply_text("Game has already started")

def new_math_game(bot,update):
    global num_GROUP
    group_id = update.message.chat_id
    if group_id not in group_lst:
        num_GROUP = group_id
        group_lst.append(group_id)
        updater.dispatcher.add_handler(CommandHandler("join_num_game",join_num_game))
        updater.dispatcher.add_handler(CommandHandler("start_num_game",start_num_game))
        updater.dispatcher.add_handler(CommandHandler("n",get_num_from_user))
        updater.dispatcher.add_handler(CommandHandler("end_num_game",end_num_game))
        update.message.reply_text("Starting new game\nType /join_num_game to join.")
    else:
        update.message.reply_text("A game is already running")


updater.dispatcher.add_handler(CommandHandler('new_num_game', new_math_game))
#updater.start_polling()
#updater.idle()
updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)

updater.bot.setWebhook('https://rajwordgamebot.herokuapp.com/' + TOKEN)

updater.idle()

