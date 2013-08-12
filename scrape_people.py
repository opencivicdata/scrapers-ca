import sys, os
import importlib
import argparse
from pupa.cli import __main__
from pupa.cli.commands import update, base
jurisdictions = os.listdir('.')
jurisdictions = [x for x in jurisdictions if os.path.exists('./'+x+'/__init__.py')]
errors = {}

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

  except:
    print '-------------------------' , sys.exc_info()

