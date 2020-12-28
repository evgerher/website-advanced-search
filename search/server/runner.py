from flask import Flask, request, json, jsonify
from flask_cors import CORS

from search.index.indexer import Index
from search.logger import setup_logger
from search.qa.engine import SimpleQA

def load_website(path):
  mapping = {}
  url_mapping = {}
  with open(path, 'r') as f:
    for idx, line in enumerate(f):
      obj = json.loads(line)
      mapping[idx] = obj
      url_mapping[obj['url']] = idx
  return mapping, url_mapping

app = Flask(__name__)
app.config['SECRET_KEY'] = '!SUPER_SECRET!'
CORS(app)

qa = SimpleQA()
index = Index('website-index')
idx_website, url_website = load_website('parsed.jsonl')

TOP_N = 3


@app.route('/connected', methods=['POST'])
def handle_user_connect():
  msg_json = request.json
  print('User connected, msg', msg_json)
  return 'OK', 200


@app.route('/phase1', methods=['POST'])
def handle_user_phase1():
  msg_json = request.json
  app.logger.info('Phase 1 request: %s', msg_json)
  user_question = msg_json['question']
  indexes, scores = index.query(user_question)

  pages = [idx_website[idx] for idx in indexes[:TOP_N]]
  print('Suggested pages: ', [page['url'] for page in pages])
  return jsonify(pages), 200

@app.route('/phase2', methods=['POST'])
def handle_user_phase2():
  msg_json = request.json
  app.logger.info('Phase 2 request: %s', msg_json)

  user_question = msg_json['question']
  url = msg_json['url']

  idx = url_website[url]
  context = idx_website[idx]['text']
  answer = qa.answer(user_question, context)
  print('Received answer: ', answer)
  return jsonify({'score': answer.score, 'answer': answer.answer}), 200



if __name__ == '__main__':
  setup_logger('cli')
  app.run(host='0.0.0.0', port=5000)