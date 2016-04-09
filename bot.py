#! /usr/bin/python
# Telegram Bot Search Package into PyPI https://pypi.python.org
# -*- coding: utf8
# Repo: https://github.com/celisflen-bers/pypi-search-pkg-bot
#
# Create by Carlos Celis Flen-Bers

import telebot, random, logging
from telebot import util
import re

# functions bot
from functions import *

user = ''
MAX_PACKAGE_RETURN = 10

# Emojis
emoji_arrow = "\xE2\x9E\xA2 "
emoji_pkg = "\xF0\x9F\x93\xA6"
emoji_ve_flag = "\xF0\x9F\x87\xBB\xF0\x9F\x87\xAA"
emoji_error= "\xE2\x9B\x94"

# Messages
text_messages = {
  'welcome':
    "Welcome *@{user}!*. I'm your new friend. Write /help for more instruccions",
  'about':
    "Hi, I'm [@PyPiDev_Bot](http://telegram.me/PyPiDev_Bot) a bot special for Python developers\n\nYour can call or share by [Telegram.me](http://telegram.me/PyPiDev_Bot)\n\nI 'm created in {ve_flag} by [@CelisFlen_Bers](http://telegram.me/CelisFlen_Bers) and my repo into [GitHub](https://github.com/celisflen-bers/pypi-search-pkg-bot)",
  'help':
    "/help this help\n/pypi find a specific package into PyPI\n/search search into PyPI\n/about about of this bot",
  'cmd_search_error':
    "{emoji_error}*ERROR*\n\nUse:\n/search TextToSearch",
  'cmd_pypi_error':
    "{emoji_error}*ERROR*\n\nUse:\n/pypi PackageToFind"
}


# Read secret token of plain text
with open("token.secret") as t:
    bot = telebot.TeleBot(t.readline().replace('\n', ''))

def formatted_text(id, message=None):
  if id == 'welcome':
    return text_messages[id].format(user=message.from_user.username)
  elif  id  == 'about':
    return text_messages[id].format(ve_flag=emoji_ve_flag)
  elif  id  == 'cmd_pypi_error':
    return text_messages[id].format(emoji_error=emoji_error)
  elif id == 'cmd_search_error':
    return text_messages[id].format(emoji_error=emoji_error)
  else:
    return text_messages[id]


#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    bot.reply_to(message, 'Command not recognized')
#    send_help(message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, formatted_text('welcome', message), parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, formatted_text('about'), parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message, text_messages['help'])


def get_arg(argument):
    regexp = re.compile("\/\w*(@\w*)*\s*([\s\S]*)",re.IGNORECASE)
    textmatch = regexp.match(argument)
    return textmatch.group(2)


@bot.message_handler(commands=['search'])
def search(message):
    argument = get_arg(message.text)
    if argument == '' or argument == None:
        bot.reply_to(message, ('cmd_search_error'))
        return
    bot.reply_to(message,locate_or_list(argument), parse_mode='Markdown')

@bot.message_handler(commands=['pypi'])
def pypi(message):
  argument = get_arg(message.text)
  if argument == '' or argument == None:
    bot.reply_to(message, formatted_text('cmd_pypi_error'), parse_mode='Markdown')
    return
  response = pkg_info(argument)
  if response != None:
    bot.reply_to(message, package_located(response), parse_mode='Markdown')
  else:
    bot.reply_to(message, package_not_found(argument), parse_mode='Markdown')
    

def package_located(pkg):
  info="{pkg}*{pkg_info[name]} {pkg_info[version]}*: _{pkg_info[summary]}_\n\nFor more information visit {pkg_info[home_page]}\nFor download {pkg_info[release_url]}".format(pkg=emoji_pkg, pkg_info=pkg)
  return info


def package_not_found(argument):
    return "The package *{argument}* not found".format(argument=argument)


def list_packages(argument):
    count = 0
    if count==0:
        return package_not_found(argument)
    elif count > MAX_PACKAGE_RETURN:
        return too_many_packages(argument,results,count)
    else:
        return package_list(argument,results,count)

def locate_or_list(argument):
#  return argument
  pkgs = pypisearch(argument)
  count_pkgs = len(pkgs)
  if count_pkgs <= MAX_PACKAGE_RETURN:
    return package_list(pkgs, count_pkgs)
  else:
    return too_many_packages(argument, pkgs, count_pkgs)

def package_list(pkgs, count):
#TODO include web link
    response = "{count} Results:\n".format(count=count) if count>1 else "{count} Result:\n".format(count=count)
    for x in pkgs:
      response += x + "\n"
    return response


def too_many_packages(argument, pkgs, count):
#TODO include web link
    response = "{} Results. *Some of them are*:\n\n".format(count)
    for x in range(MAX_PACKAGE_RETURN):
      response += " {pkg} *{results[name]} {results[version]}*:  _{results[summary]}_\n\n".format(pkg=emoji_pkg, results=random.choice(pkgs))
    response += "\n To see the rest visit [Pypi](https://pypi.python.org/pypi?%3Aaction=search&term={package}&submit=search)".format(package=argument)
    return response


if __name__=="__main__":
    bot.polling()
    # getMe
    user = bot.get_me()
