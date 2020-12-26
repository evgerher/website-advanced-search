import logging
import logging.config
import os

import yaml

def setup_logger(default_path='logging.yaml', default_level=logging.INFO):
  if os.path.exists(default_path):
    with open(default_path, 'rt') as f:
      try:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
      except Exception as e:
        print(f'Error in Logging Configuration. Using default configs; error: {e}')
        logging.basicConfig(level=default_level)
  else:
    logging.basicConfig(level=default_level)
    print('Failed to load configuration file. Using default configs')