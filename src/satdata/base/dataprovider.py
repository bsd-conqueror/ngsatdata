#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from satdata.base.errors import *

http_5xx_codes = [500, 501, 502, 503, 504, 511, 520, 521, 522, 525, 530]
http_4xx_codes = [400, 401, 403, 405, 408, 421, 422]
http_2xx_codes = [200, 201, 202]


class DataProvider(object):
    api_key = None
    api_secret = None
    timeout = 3  # 3 seconds
    response = None
    request = None
    logger = None
    session = None
    auth_url = None
    api_url = None

    def __init__(self, log_level=logging.INFO):
        self.logger = self.get_logger(__name__, log_level)

    def get_logger(self, module_name='satdata', log_level=logging.INFO):
        logger = logging.getLogger(module_name)
        if not getattr(logger, 'handler_set', None):
            # get the log level of specified module and set it
            logger.setLevel(log_level)
            # stomp = {'host': '127.0.0.1', 'port': 61613, 'login': 'guest', 'password': 'guest', 'queue' : '/topic/kp'}
            # create console handler and set level to debug

            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            formatter = logging.Formatter(
                fmt='[%(asctime)s] %(name)s: %(lineno)d: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            console_handler.setFormatter(formatter)

            # add fh to logger
            logger.addHandler(console_handler)

            logger.handler_set = True
        return logger

    def get_sources(self):
        pass

    def get_instruments(self):
        pass

    def get_channels(self):
        pass

    def fetch(self, api_url, method='GET', headers={}, payload={}):
        if method == 'GET':
            r = self.session.get(api_url, headers=headers, params=payload)
            if r.status_code in http_2xx_codes:
                return r.text
            elif r.status_code in http_4xx_codes:
                self.logger.error('Access denied. URL: %s, method: %s, headers: %s, payload: %s' % (
                    api_url,
                    method,
                    headers,
                    payload
                ))
                raise AccessDenied('URL: %s, method: %s' % (api_url, method))
        elif method == 'POST':
            # print(self.session.cookies)
            r = self.session.post(api_url, headers=headers, data=payload, cookies=self.session.cookies)
            if r.status_code in http_2xx_codes:
                return r.text
            elif r.status_code in http_4xx_codes:
                self.logger.error('Access denied. URL: %s, method: %s, headers: %s, payload: %s' % (
                    api_url,
                    method,
                    headers,
                    payload
                ))
                raise AccessDenied('URL: %s, method: %s' % (api_url, method))
        else:
            raise MethodNotSupported('URL: %s, method: %s' % (api_url, method))

    def authorize(self):
        #self.logger.debug('Authorizing with %s...' % self.auth_url)
        pass
