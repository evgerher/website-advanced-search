import logging
from typing import TextIO, Tuple, Iterable, Optional
from abc import ABC
import xml.etree.ElementTree as ET
import json

from bs4 import BeautifulSoup

URL = TITLE = CONTENT = str

logger = logging.getLogger('cli')


class BaseRule(ABC):
  @staticmethod
  def extract_data(page: BeautifulSoup) -> CONTENT:
    raise NotImplementedError

  @staticmethod
  def extract_title(page: BeautifulSoup) -> TITLE:
    raise NotImplementedError


class SallysBakingAddictionRule(BaseRule):
  """
  Named so by the website I am interested in
  """

  @staticmethod
  def extract_data(page: BeautifulSoup) -> Optional[CONTENT]:
    texts = []
    noisy_artefact = '\xa0'


    paragraphs = page.find('div', {"class": "entry-content"})
    if paragraphs is not None:
      paragraph_texts = paragraphs.find_all('p')

      # Cook's comments
      for paragraph in paragraph_texts:
        text = paragraph.text
        if len(text) > 0:
          if not text.startswith('Tag @sallysbakeblog'):
            texts.append(text.replace(noisy_artefact, ' '))

    # ingredient text
    recipe = page.find('div', {'class': 'tasty-recipes'})

    if recipe is None and paragraphs is None:
      return None

    if recipe is not None:
      recipe_text = recipe.text.replace(noisy_artefact, ' ')
      texts += [recipe_text]

    return ' '.join(texts)


  @staticmethod
  def extract_title(page: BeautifulSoup) -> TITLE:
    return page.h1.text or ''


def parse_html(crawler_filepath: str, output_file: TextIO):
  root = ET.parse(crawler_filepath).getroot()
  triplets = extract_information(root, SallysBakingAddictionRule)
  for (url, title, text) in triplets:
    obj = {'url': url, 'title': title, 'text': text}
    json.dump(obj, output_file)
    output_file.write('\n')


def extract_information(root: ET.Element, rule: BaseRule.__class__) -> Iterable[Tuple[URL, TITLE, CONTENT]]:
  items = root.findall('item/content')
  urls = root.findall('item/url')

  for idx, (url, html_text) in enumerate(zip(urls, items)):
    url = url.text
    logger.info('%d. Parsed url: %s', idx, url)
    page = BeautifulSoup(html_text.text, 'html.parser')
    title = rule.extract_title(page)
    text = rule.extract_data(page)


    if text is not None:
      yield (url, title, text)
