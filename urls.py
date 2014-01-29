import importlib
import os
import os.path

for module_name in os.listdir('.'):
  if os.path.isdir(module_name) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
    module = importlib.import_module(module_name)
    for obj in module.__dict__.values():
      jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
      if jurisdiction_id:  # We've found the module.
        print '%-60s %s' % (module_name, getattr(obj, 'url', None))
