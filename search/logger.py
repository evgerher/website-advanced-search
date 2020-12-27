import logging
import logging.config
import os

import yaml

# def setup_logger(default_path='logging.yaml', default_level=logging.INFO):
  # if os.path.exists(default_path):
  #   with open(default_path, 'rt') as f:
  #     try:
  #       config = yaml.safe_load(f.read())
  #       logging.config.dictConfig(config)
  #     except Exception as e:
  #       print(f'Error in Logging Configuration. Using default configs; error: {e}')
  #       logging.basicConfig(level=default_level)
  # else:
  #   logging.basicConfig(level=default_level)
  #   print('Failed to load configuration file. Using default configs')

def setup_logger(name, default_path='logging.yaml', default_level=logging.INFO):
  formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
  )

  all_file_handler = logging.FileHandler(
    filename='application.log'
  )
  all_file_handler.setLevel(logging.DEBUG)
  all_file_handler.setFormatter(formatter)

  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  logger.addHandler(all_file_handler)
