# Funciones para PyVeBot
# -*- coding: utf8
# Mas info https://github.com/pyve/PyVenezuelaBot

# Creado por Carlos Celis Flen-Bers
# Repo: https://github.com/celisflen-bers/pyvebot_functions

import xmlrpclib
import re
from lxml.etree import fromstring
from lxml.cssselect import CSSSelector

MAX_PACKAGE_RETURN = 50

pypi_base_url   = "https://pypi.python.org/"
pypi_index = pypi_base_url + "pypi/"

pypi_simple_url = pypi_base_url + "simple/index.html"
# wget https://pypi.python.org/simple/index.html -O simple.html
pypi_simple_local = "simple.html"

with open(pypi_simple_local) as f:
  h = fromstring(f.read())
  sel = CSSSelector("a")
  packages = {}
  for e in sel(h):
    packages[e.text] = e.get("href")


# XMLRPC connection
def srv_conn():
  # https://wiki.python.org/moin/PyPIXmlRpc
  srv_pypi = xmlrpclib.ServerProxy(pypi_index)
  return srv_pypi


# Multi match
def simple_search(pkg):
  # https://wiki.python.org/moin/PyPISimple
  results = {}
  regexp = re.compile(pkg, re.IGNORECASE)
  for x in packages:
    if regexp.search(x) is not None:
      results[x] = packages[x]
  return results


# Función pypi en el bot
def pkg_info(pkg):
  # https://wiki.python.org/moin/PyPIXmlRpc
  rel_len = 0
  res = simple_search(pkg)
  res_len = len(res)
  if res_len > 0:
    pkg_info = srv_conn()
    rel = pkg_info.package_releases(pkg)
    rel_len = len(rel)
    pkg_data = None
    if rel_len > 0:
      lastest_rel = rel and rel[0] or None
      pkg_data = pkg_info.release_data(pkg, lastest_rel)
    return pkg_data


# Función pysearch en el bot
def xmlrpcsearch(pkg, spec='name'):
  # https://wiki.python.org/moin/PyPIXmlRpc
  pkg_info = srv_conn()
  return pkg_info.search({'name':pkg}, {'_pypi_ordering': True})
