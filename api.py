# -*- coding: utf-8 -*-
# Simple Pantera API

import io
import time
import json
import os
from io import StringIO, BytesIO
from subprocess import check_output

# Import framework
import six
from flask import Flask
from flask_restful import Resource, Api, abort, request, reqparse
from lxml import etree

# Instantiate the app
app = Flask(__name__)
api = Api(app)

formats_files = {
    'nkjp': 'ann_morphosyntax.xml',
    'xces': 'a.txt.disamb',
    'xces-disamb': 'a.txt.disamb',
}

exe = 'pantera' if os.path.exists('/.dockerenv') else './pantera'


def run_pantera(text, format='nkjp'):
    out_file = formats_files[format]

    with io.open('a.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    log = check_output([exe, '-o', format, 'a.txt'])

    with io.open(out_file, encoding='utf-8') as f:
        out = f.read()

    return out


class Pantera(Resource):
    arg_parser = reqparse.RequestParser()
    arg_parser.add_argument('text', type=unicode if six.PY2 else str, required=True)
    arg_parser.add_argument('format', type=str, default='nkjp')

    """Runs pantera and returns the output."""
    def get(self):
        args = self.arg_parser.parse_args()
        text = args['text']
        out_format = args['format']
        if out_format not in formats_files:
            abort(400, message="Wrong format: '%s'!" % out_format)

        start = time.time()
        out = run_pantera(text, format=out_format)
        end = time.time()
        return {'xml': out, 'time': end-start}


class SimplePantera(Resource):
    """Send a 'list' of paragraphs. Get a list of disambiguated tokens.

       If any entry contains "\n\n" it will be considered as another paragraph,
       and the returned list will be of different lenght than the source.
       Set 'sentences': True to get a separate list for every sentence."""

    arg_parser = reqparse.RequestParser()
    arg_parser.add_argument('list', action='append', required=True)
    smart_bool = lambda b: False if b in ('False', '0') else bool(b)
    arg_parser.add_argument('sentences', type=smart_bool, default=False)

    def get(self):
        args = self.arg_parser.parse_args()

        text = '\n\n'.join(args['list'])
        separate_sents = args['sentences']

        start = time.time()
        xml = run_pantera(text, format='xces-disamb')

        parser = etree.XMLParser(recover=True)
        T = etree.parse(BytesIO(xml.encode('utf-8')), parser)
        res = []
        for P in T.xpath('.//chunk[@type="p"]'):
            res.append([S.xpath('.//lex[@disamb="1"]/base/text()')
                        for S in P.xpath('.//chunk[@type="s"]')])
        end = time.time()

        if not separate_sents:
            res = [sum(p, []) for p in res]

        return {'list': res, 'time': end-start}

# Create routes
api.add_resource(Pantera, '/')
api.add_resource(SimplePantera, '/simple')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
