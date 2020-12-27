import logging
from typing import TextIO, List
import json
import pickle
import re
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse
import spacy
import numpy as np


logger = logging.getLogger('cli')

PATTERN = re.compile(r'[0-9][^ ]*')
PUNCTUATION_TABLE = str.maketrans('', '', string.punctuation)

LEMMA = str

class Index:
  def __init__(self, index_filepath: str):
    self._nlp = spacy.load('en_core_web_md')

    matrix_path = index_filepath + '.npz'
    vectorizer_path = index_filepath + '-vectorizer.pkl'
    words_path = index_filepath + '-words.txt'

    self._corpus_matrix: TfidfVectorizer = scipy.sparse.load_npz(matrix_path)
    with open(vectorizer_path, 'rb') as vectorizer_f, open(words_path, 'r') as words_f:
      self._vectorizer: TfidfVectorizer = pickle.load(vectorizer_f)
      self._word_set = set([w.rstrip() for w in words_f.readlines()])

  def query(self, query: str):
    logger.info('Received query: <%s>', query)
    lemmas = transform_text(self._nlp, query)
    lemma_text = ' '.join([lemma for lemma in lemmas if lemma in self._word_set])
    vector = self._vectorizer.transform([lemma_text])
    similarities = cosine_similarity(vector, self._corpus_matrix)
    indexes = np.argsort(-similarities, )
    scores = similarities[0, indexes]
    return indexes, scores


def transform_text(nlp, text: str) -> List[LEMMA]:
  text = text.lower().replace("\n", " ").replace("’", "")
  text = text.translate(PUNCTUATION_TABLE)
  text = re.sub(PATTERN, ' ', text)
  tokens = nlp(text)
  return [token.lemma_ for token in tokens if token.is_alpha and not (token.is_stop or token.is_punct or token.is_digit or '0' <= token.text[0] <= '9')]


def build_index(input_file: TextIO, index_output_filepath: str):
  nlp = spacy.load('en_core_web_md')
  logger.info('Loaded spacy engine.')

  corpus = []
  for idx, row in enumerate(input_file, 1):
    # {'url': url, 'title': title, 'text': text}
    line = json.loads(row)
    text = f"{line['title']} {line['text']}".lower()
    lemmas = transform_text(nlp, text)
    corpus += [' '.join(lemmas)]

  n_documents = idx
  logger.info('Trasnformed %d texts with SpaCy.', n_documents)

  vectorizer = TfidfVectorizer(max_features=100_000)
  corpus_vectored = vectorizer.fit_transform(corpus)
  present_words = vectorizer.get_feature_names()
  logger.info('Created tf-idf vectorizer and transformed text corpus.')

  matrix_path = index_output_filepath + '.npz'
  scipy.sparse.save_npz(matrix_path, corpus_vectored)
  logger.info('Stored sparse matrix at %s.', matrix_path)

  vectorizer_path = index_output_filepath + '-vectorizer.pkl'
  with open(vectorizer_path, 'wb') as f:
    pickle.dump(vectorizer, f)
  logger.info('Stored vectorizer at %s.', vectorizer_path)

  words_path = index_output_filepath + '-words.txt'
  with open(words_path, 'w') as f:
    for word in present_words:
      f.write(f'{word}\n')
  logger.info('Stored words at %s.', words_path)
