# Funciones para PyVeBot
# -*- coding: utf8
# Creado por Carlos Celis Flen-Bers
# Repo: https://github.com/celisflen-bers/pypi-search-pkg-bot

import telebot, random
from telebot import util
from lxml.etree import fromstring
from lxml.cssselect import CSSSelector
import re
import xmlrpclib

MAX_PACKAGE_RETURN = 10
pypi_base_url = "https://pypi.python.org/pypi/"

with open("token.secret") as t:
    bot = telebot.TeleBot(t.readline().replace('\n', ''))

with open("simple.html") as f:
    h = fromstring(f.read())
    sel = CSSSelector("a")
    packages = []
    for e in sel(h):
        packages.append(e.get("href"))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola! Estoy a tu servicio. Para una lista de comandos escribe /help, soy un bot en construccion")

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, "Hola! Soy PyVeBot!\nSoy un bot para hacer mas simple la busqueda y enlace a paquetes del repositorio PyPi!\nFui creado por @CelisFlen_Bers y tengo un repositorio con mi codigo fuente en https://github.com/celisflen-bers/pypi")

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message,"/help para esta ayuda\n/pypi para link directo\n/pysearch para busqueda de paquete\n/about sobre este bot")

@bot.message_handler(commands=['pypi'])
def pypi(message):
    argument = get_arg(message.text)
    if argument == '' or argument == None:
        return
    bot.reply_to(message,locate_or_list(argument))

@bot.message_handler(commands=['pysearch'])
def pysearch(message):
    argument = get_arg(message.text)
    if argument == '' or argument == None:
        return
    response = list_packages(argument)
    splitted_text = util.split_string(response, 3000)
    for text in splitted_text:
        bot.reply_to(message,text)

def get_arg(argument):
    regexp = re.compile("\/\w*(@\w*)*\s*([\s\S]*)",re.IGNORECASE)
    textmatch = regexp.match(argument)
    return textmatch.group(2)

def list_packages(argument):
    count = 0
    results = []
    regexp = re.compile(argument,re.IGNORECASE)
    for x in packages:
        if regexp.search(x) is not None:
            results.append(x)
            count+=1
    if count==0:
        return package_not_found(argument)
    elif count > MAX_PACKAGE_RETURN:
        return too_many_packages(argument,results,count)
    else:
        return package_list(argument,results,count)

def locate_or_list(argument):
    if argument.lower() in packages:
      return package_located(argument)
    regexp = re.compile(argument,re.IGNORECASE)
    count = 0
    results = []
    for x in packages:
        if regexp.search(x) is not None:
            results.append(x)
            count+=1
    if count==0:
        return package_not_found(argument)
    elif count > MAX_PACKAGE_RETURN:
        return too_many_packages(argument,results,count)
    else:
        return package_list(argument,results,count)

def package_located(argument):
    info = {}
    info['url'] = str(pypi_base_url + argument)
    
    # Using https://wiki.python.org/moin/PyPIXmlRpc
    pkg_info = xmlrpclib.ServerProxy(pypi_base_url)
    
    rel = pkg_info.package_releases(argument)
    info['lastest_rel'] = rel[0]
    
    pkg_data = pkg_info.release_data(argument, info['lastest_rel'])
    info['name'] = pkg_data['name']
    info['summary'] = pkg_data['summary']

    return info

def package_not_found(argument):
    return "Su busqueda regreso 0 resultados"

def package_list(argument,results,count):
    response = "{} Resultados:\n".format(count) if count>1 else "{} Resultado:\n".format(count)
    for x in results:
      response += x + "\n"
    return response

def too_many_packages(argument,results,count):
    response = "{} Resultados:\nAlgunos de estos son:\n".format(count)
    for x in range(MAX_PACKAGE_RETURN):
      response += random.choice(results) + "\n"
    return response

if __name__=="__main__":
    bot.polling()
