import sys, os
import importlib
import argparse
from mycityhall_scrapers import *
from pupa.cli import __main__
from pupa.cli.commands import update, base

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mycityhall_scraperreports.settings")


def scrape_people():
  jurisdictions = os.listdir('./mycityhall_scrapers')
  # scraper_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))+'/mycityhall_scrapers/'
  scraper_path = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))+'/'
  print scraper_path
  sys.path.insert(0,scraper_path)
  jurisdictions = [x for x in jurisdictions if os.path.exists(scraper_path+x+'/__init__.py')]


  reports = []


  for jurisdiction in jurisdictions:
    try:
      COMMAND_MODULES = (
          'pupa.cli.commands.update',
      )
      parser = argparse.ArgumentParser('pupa', description='pupa CLI')
      subparsers = parser.add_subparsers(dest='subcommand')

      subcommands = {}
      for mod in COMMAND_MODULES:
        cmd = importlib.import_module(mod).Command(subparsers)
        subcommands[cmd.name] = cmd

      # process args
      args = parser.parse_args(['update', '--people', jurisdiction])
      subcommands[args.subcommand].handle(args)

      report = {'name' : jurisdiction, 'status' : 'working', 'error' : 'none' }
      reports.append(report)

    except:
      report = {'name' : jurisdiction, 'status' : 'working' , 'error' : sys.exc_info()}
      reports.append(report)
  return reports
