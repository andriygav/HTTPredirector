# -*- coding: utf-8 -*- 
from configobj import ConfigObj

from functools import partial, wraps
from subprocess import PIPE, Popen
import requests
import logging
import yaml
import sys
import os
import io

from flask import (render_template, Flask, request, 
                   Response, redirect, flash, url_for, send_file)
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s:%(funcName)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

def init(config, setup):
    config = ConfigObj(infile=config, encoding='utf-8')
    with open(setup) as f:
        setup = yaml.safe_load(f)

    app.secret_key = config['app']['secret_key']
    csrf.init_app(app)

    for item in setup['urls']:
        path = os.path.join('/', *(item['name']).split('/'), *(item['path']).split('/'))
        headers = dict()
        for header in item['headers']:
            prefix = header['valueBegin']
            sufix = header['valueEnd']
            if 'valueFrom' in header:
                try:
                    with open(header['valueFrom']) as f:
                        value = f.read()
                except Exception as e:
                    logging.info(str(e))
                    value = ''
            headers[header['key']] = prefix+value+sufix

        app.add_url_rule(
            path, 
            path.replace('/', '-'),
            partial(
                func, 
                args=item['args'],
                host=item['host'],
                headers=headers))
        logging.info(f'Add rule path {path}')
    return app

def func(host, headers, args, **argv):
    params = dict()
    for arg in args:
        params[arg] = request.args.get(arg)

    resp = requests.get(host, headers=headers, params=params, verify=False)
    return (resp.text, resp.status_code, resp.headers.items())