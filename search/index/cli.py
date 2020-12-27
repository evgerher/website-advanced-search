from argparse import ArgumentParser, FileType
import logging

from search.index import html_parser as hp
from search.index import indexer as ix
from search.logger import setup_logger

logger = logging.getLogger('cli')


def html_parser_callback(args):
  logger.info('Received args: %s', args)
  hp.parse_html(args.crawler_filepath, args.output_file)


def build_index_callback(args):
  logger.info('Received args: %s', args)
  ix.build_index(args.input_file, args.output_filepath)


def parse_arguments():
  main_argparser = ArgumentParser('Inverted index builder.')
  subparsers = main_argparser.add_subparsers(help='Choose command to use')

  html_parser = subparsers.add_parser('parse')
  html_parser.add_argument('-i', '--crawler_filepath',
                      required=True,
                      type=str,
                      dest='crawler_filepath',
                      metavar='/path/to/file',
                      help='Path to crawler results (file)')

  # todo: require target file to import and use as a parsing rule (just like `scrapy` does)

  html_parser.add_argument('-o', '--output_file',
                      required=True,
                      type=FileType('w', encoding='utf-8'),
                      dest='output_file',
                      metavar='/path/to/output.jsonl',
                      help='Path for extracted data to store (jsonl)')
  html_parser.set_defaults(callback=html_parser_callback)

  index_builder = subparsers.add_parser('build')
  index_builder.add_argument('-i', '--input_file',
                             required=True,
                             dest='input_file',
                             metavar='/path/to/file.txt',
                             help='Path to extracted data from `parse` step.',
                             type=FileType('r', encoding='utf-8'))
  index_builder.add_argument('-o', '--output',
                             type=str,
                             required=False,
                             dest='output_filepath',
                             default='website.index',
                             metavar='/path/to/index',
                             help='Path for a number of generated files (-matrix.npz, -words.txt, ...)')
  index_builder.set_defaults(callback=build_index_callback)

  return main_argparser.parse_args()


if __name__ == '__main__':
  setup_logger('cli')
  arguments = parse_arguments()
  arguments.callback(arguments)
