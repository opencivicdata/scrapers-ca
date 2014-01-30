import importlib
import os
import os.path

for module_name in os.listdir('.'):
  if os.path.isdir(module_name) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
    module = importlib.import_module('%s.people' % module_name)
    print '%-60s %s' % (module_name, module.__dict__['COUNCIL_PAGE'])
