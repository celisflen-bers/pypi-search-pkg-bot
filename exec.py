#!/usr/bin/python
# -*- coding: utf8
# Carlos Celis Flen-Bers

import sys, getopt, random
from itertools import islice
from functions import *

help_msg = "Execute:\n" + sys.argv[0] + " <package>"


def usage():
  print help_msg


def about():
  print "Programa de ejecución"


def salida():
  about()
  sys.exit()
  

def error_msg(error_status, str_search, count):
  error_msg = {}
  error_msg[0] = "No problem! ;-)"
  error_msg[1] = "No se encontró el paquete: {} pero se encontraron {} parecidos".format(str_search, count)
  error_msg[2] = "No se encontró el paquete: " + str_search + " ni nada parecido"
  return error_msg[error_status]


def pysearch(pkg='pypi'):
  # En representación del bot
  res = pypisearch(pkg)
  for i in res:
    print '  -{name}: {version}\n    {summary}'.format(name=i['name'],version=i['version'],summary=i['summary'])


def print_info_pkg(name, url):
  print "  * {}\n      URL= {}{}".format(name, pypi_base_url, url)

def pypi(pkg='pypi'):
  # En representación del bot

  res = pkg_info(pkg)
  if res != None:
  
    print '  {name}: {version}'.format(name=res['name'], version=res['version'])
    print '    {summary}'.format(summary=res['summary'])
    print '  Visite {pkg_url} para ver paquete pypi'.format(pkg_url=res['package_url'])
    print '  Visite {home_page} para más info'.format(home_page=res['home_page'])

  else:
    # parecida
    # TODO busqueda como pip search
    error_status = 2
    print error_msg(error_status, pkg, 0)


def take(n, iterable):
  #https://docs.python.org/2/library/itertools.html#recipes
  "Return first n items of the iterable as a list"
  return list(islice(iterable, n))


def too_many_packages(results):
  response = '' #"{} Resultados:\nAlgunos de estos son:\n".format(count)
  keys = results.keys()
  random.shuffle(keys)
  truncate_res = take(MAX_PACKAGE_RETURN, results.iteritems())
  return truncate_res
    

def main(argv):
  package = ''
  try:
    opts, args = getopt.getopt(argv,"hp:i:l",["help", "about", "pysearch=", "pypi=","list"])
  except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt == '--about':
      salida()
    elif opt in ("-p", "--pysearch"):
      print "pysearch: " + repr(arg)
      if arg == '' or arg == None:
        salida()
      pysearch(arg)
    elif opt in ("-i", "--pypi"):
      print "pypi: " + repr(arg)
      if arg == '' or arg == None:
        salida()
      pypi(arg)
    elif opt in ("-l", "--list"):
      print "Visit https://pypi.python.org/simple/"

if __name__ == "__main__":
  main(sys.argv[1:])
