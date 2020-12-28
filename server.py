from search.logger import setup_logger
from search.server.runner import app

if __name__ == '__main__':
  setup_logger('cli')
  app.run(host='0.0.0.0', port=5001)