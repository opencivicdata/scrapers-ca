import sys, os
jurisdictions = os.listdir('.')
jurisdictions = [x for x in jurisdictions if os.path.exists('./'+x+'/__init__.py')]
errors = {}
for jurisdiction in jurisdictions:
  try:
    os.system("python -m pupa.cli update --people "+jurisdiction)
  except:
    errors[jurisdiction] = sys.exc_info()[0]
    print '----------------------------------'
for key, value in errors.iteritems():
  print key, ' failed with ', value
