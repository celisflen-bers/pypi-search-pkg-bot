# Bot Functions
# -*- coding: utf8
# Repo: https://github.com/celisflen-bers/pypi-search-pkg-bot

# Create by Carlos Celis Flen-Bers

#from pypixmlrpc import *
from pkgtools.pypi import PyPIXmlRpc

MAX_PACKAGE_RETURN = 50

pypi_base_url   = "https://pypi.python.org/"
pypi_index = pypi_base_url + "pypi/"


# Función pypi en el bot
def pkg_info(pkg):
  # https://wiki.python.org/moin/PyPIXmlRpc
  pypi = PyPIXmlRpc()
  rel = pypi.package_releases(pkg)
  rel_len = len(rel)
  pkg_data = None
  if rel_len > 0:
    lastest_rel = rel and rel[0] or None
    pkg_data = pypi.release_data(pkg, lastest_rel)
  return pkg_data


# Función pysearch en el bot
def pypisearch(pkg):
  pypi = PyPIXmlRpc()
  # https://wiki.python.org/moin/PyPIXmlRpc
  return pypi.search({'name':pkg, 'summary':pkg}, 'or')
