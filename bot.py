import logging
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import json
import imdb
import os

BOT_TOKEN = "5162967266:AAHPk74BQBUbz9Uuh4u7G5TxvsULWpvveGo"
OMDB_API_KEY = '558c75c8'

ia = imdb.IMDb() 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi! \nWelcome to the *IMDb Bot*. \nSend me the name of any movie or TV show to get its details. \nHappy viewing! \n \nCreated by [Karan Malik](https://karan-malik.github.io)',parse_mode='markdown')


def help(update, context):
    update.message.reply_text('Send me the name of any movie to get its details. \nTry out "Avengers Endgame"')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def reply(update, context):
    movie_name=update.message.text
    search = ia.search_movie(movie_name)
      
    id='tt'+search[0].movieID
    
    url= 'http://www.omdbapi.com/?i='+id+'&apikey='+OMDB_API_KEY
    
    x=urllib.request.urlopen(url)
    
    for line in x:
        x=line.decode()
    
    data=json.loads(x)
    
    ans=''
    ans+='*'+data['Title']+'* ('+data['Year']+')'+'\n\n'
    ans+='*IMDb Rating*: '+data['imdbRating']+' \n'
    ans+='*Cast*: '+data['Actors']+'\n'
    ans+='*Genre*: '+data['Genre']+'\n\n'
    ans+='*Plot*: '+data['Plot']+'\n'
    ans+='[.]('+data['Poster']+')'
    update.message.reply_text(ans,parse_mode='markdown')  


def main():

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 
