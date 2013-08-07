import sys, os
jurisdictions = os.listdir('.')
jurisdictions = [x for x in jurisdictions if os.path.exists('./'+x+'/__init__.py')]
for jurisdiction in jurisdictions:
  os.system("python -m pupa.cli update --people "+jurisdiction)