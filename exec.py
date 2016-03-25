#!/usr/bin/python
# -*- coding: utf8
# Carlos Celis Flen-Bers

import sys, getopt, random
from itertools import islice
from functions import *

help_msg = "Exec\n" + sys.argv[0] + " <package>"


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
  res = xmlrpcsearch(pkg)
  for i in res:
    print '  -' + i['name'] + ': ' + i['version'] + '\n    ' + i['summary']


def print_info_pkg(name, url):
  print "  * {}\n      URL= {}{}".format(name, pypi_base_url, url)

def pypi(pkg='pypi'):
  # En representación del bot

  res_search = pkg in packages

  if res_search == True:
    res = pkg_info(pkg)
    print '  ' + res['name'] + ': ' + res['version']
    print '    ' + res['summary']
    print '  Visite {} para ver paquete pypi'.format(res['package_url'])
    print '  Visite {} para más info'.format(res['home_page'])
  else:
    # parecida
    res = simple_search(pkg)
    res_len = len(res)
    if res_len > 0:
      error_status = 1
      print error_msg(error_status, pkg, res_len)
      for p in res:
        print_info_pkg(p, res[p])
    else:
      # TODO busqueda como pip search
      error_status = 2
      print error_msg(error_status, pkg, res_len)


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
    

def simple(pkg='pypi'):
  # En representación del bot
  error_status = 0 # No error

  res = simple_search(pkg)
  res_len = len(res)
  if res_len == 0:
    error_status = 1
    print error_msg(error_status, pkg)
  elif res_len <= MAX_PACKAGE_RETURN:
    print "Su búsqueda por {} arrojó {} resultados:".format(pkg, res_len)
    for p in res:
      print_info_pkg(p, res[p])
  else:
    print "{} Resultados:\nAlgunos de estos son:\n".format(res_len)
    truncate_res = too_many_packages(res)
    for p in range(MAX_PACKAGE_RETURN):
      print_info_pkg(truncate_res[p][0], truncate_res[p][1])


def main(argv):
  package = ''
  try:
    opts, args = getopt.getopt(argv,"hp:i:s:",["help", "about", "pysearch=", "pypi=", "simple="])
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
    elif opt in ("-s", "--simple"):
      print "Simple: " + repr(arg)
      if arg == '' or arg == None:
        salida()
      simple(arg)


if __name__ == "__main__":
  main(sys.argv[1:])
