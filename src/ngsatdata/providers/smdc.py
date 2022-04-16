# -*- coding: utf-8 -*-

import json
import logging
import os
import traceback
from datetime import datetime
from typing import Dict

import pandas
import requests
import six

from ngsatdata.base.dataprovider import DataProvider
from ngsatdata.base.errors import *

from .source import Source

# -------- GLOBAL VARIABLES -------- #
default_config_file = 'smdc_config.json'
config_file = os.environ.get('SMDC_CONFIG_JSON', default_config_file)
satellite_2_noradid = {
    'soho': 23726,
    'sdo': 36395,
    'ace': 24912,
    'goes13': 29155,
    'goes14': 35491,
    'goes15': 36411,
    'meteor_m1': 35865,
    'goes15': 36411,
    'meteor_m1': 35865,
    'meteor_m2': 40069,
    'electro_l1': 37344,
    'electro_l2': 41105,
    'lomonosov': 41464,
    'dscovr': 40390,
    'vernov': 40070,
}
time_frames = ['1s', '10s', '1m', '5m', '10m', '1h', '6h', 'auto']
dt_format = '%Y-%m-%d %H:%M:%S'
# -------- END OF GLOBAL VARIABLES -------- #


class SMDC(DataProvider):
    """The driver to work with the SMDC provider

    Attributes:
        logger (obj): The internal Python logging object.
        auth_url (str): The URL for authorization.
        api_url (str): The URL for api access
        auth_input_form (dict): 
        cookie_names (dict):
    
    Usage example:
        from ngsatdata.providers.smdc import SMDC
        smdc = SMDC()
        smdc.authorize()
        df = smdc.fetch(source='electro_l2',
                        instrument='skl',
                        channel='das3vrt1',
                        start_dt='2017-10-14 10:43:38',
                        end_dt='2017-10-14 10:43:47',
                        time_frame='1s',
                        level='default')
    """
    # smdc auth credential related
    auth_input_form: Dict = {
        'username': None,
        'password': None,
        'csrfmiddlewaretoken': None
    }
    cookie_names: Dict = {
        'sid': 'sessionid',
        'csrf': 'csrftoken'
    }
    headers: Dict = {}
    metadata: Dict = {
        # fill the metadata with data from the provider
    }

    def __init__(self, base_url: str = 'http://localhost:8000', log_level: int = logging.INFO):
        self.logger = self.get_logger(module_name=__name__, log_level=log_level)
        if base_url:
            self.base_url = base_url
            self.auth_url = self.base_url + '/accounts/login/'
            self.api_url = self.base_url + '/db_iface/api/v2/'
            self.metadata_url = self.base_url + '/db_iface/api/v1/full/'
            self.headers = {
                'referer': self.base_url + '/accounts/login/'
            }


    def authorize(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if config_file == default_config_file:
            config_path = os.path.join(cur_dir, config_file)
        else:
            config_path = config_file
        if not os.path.exists(config_path):
            raise AuthConfigNotFound(
                'Please create a file called %s, put auth credentials there, and export SMDC_CONFIG_JSON=`pwd`/%s' % (config_file, config_file))

        with open(config_path, 'r') as f:
            auth_obj = json.load(f)
            if 'username' not in auth_obj or 'password' not in auth_obj:
                raise AuthCredentialsNotFound('Please specify username and password in the config file')

        self.auth_input_form['username'] = auth_obj['username']
        self.auth_input_form['password'] = auth_obj['password']

        super(SMDC, self).authorize()
        self.session = requests.Session()
        # use get to retrieve the csrf token
        self.session.get(self.auth_url)
        # set the csrf token
        if self.cookie_names['csrf'] not in self.session.cookies.keys():
            message = 'Error retrieving csrf token'
            # self.logger.debug(message)
            raise AuthenticationError(message)

        self.auth_input_form['csrfmiddlewaretoken'] = self.session.cookies[self.cookie_names['csrf']]

        # authorize with the backend
        r = self.session.post(self.auth_url, data=self.auth_input_form, headers=self.headers)
        if r.status_code == 200 and self.cookie_names['sid'] in self.session.cookies.keys():
            #self.logger.debug(self.cookie_names['sid'] + '=' + self.session.cookies[self.cookie_names['sid']])
            #self.logger.debug(self.cookie_names['csrf'] + '=' + self.session.cookies[self.cookie_names['csrf']])
            #self.logger.debug('Logged in to %s' % self.auth_url)
            return True
        else:
            message = 'Error logging in to %s. Invalid credentials' % self.auth_url
            # self.logger.debug(message)
            raise AuthenticationError(message)

    def get_sources(self):
        response = self.session.get(self.metadata_url, headers=self.headers)
        metadata = response.json()
        return [Source(codename=codename, metadata=source_metadata)
                for codename, source_metadata in metadata['data'].items()]

    def fetch(self, source, instrument, channel, start_dt, end_dt, time_frame, level='default', *args, **kargs):
        """Fetching data from a column of a table in a schema for a time interval with specific time frame


        Example payload
        {
          "where": {
            "resolution":"10m",
            "min_dt":"2014-06-06 00:00:00",
            "max_dt":"2014-06-11 23:59:59"
          },
          "options": {"unformated":"true"},
          "select": [
            "coord.meteor_m1_coord_10m.l",
            "35865.skl.das1vrt1",
            "35865.skl.das1vrt2",
            "35865.skl.das1vrt3"
          ]
        }

        Args:
          source (str): satellite name or norad id or 'models'
          instrument (str): satellite instrument name or a physical model name
          channel (str): channel name of an instrument or model
          start_dt (datetime or str): datetime object or datetime string which defines the start timestamp of a interval
          end_dt (datetime or str): datetime object or datetime string which defines the end timestamp of a interval
          time_frame (str): time frame. Possible values are 'h6', 'h1', 'm10', 'm5', 'm1', 's10', 's1', 'ms100', or 'auto'
          level (str): data level. Possible values are raw (or level0), level1a, level1b, level1, level2
        Returns:
          a Pandas Data Frame that contains the data provided by the data provider

        Raises:
          AccessDenied
          MethodNotSupported
        """

        try:
            query = self._form_query(source, instrument, channel, start_dt, end_dt, time_frame, level)
            headers = {
                'Accept': 'application/json',
                'Content-type': 'application/json',
                # 'Cookie': '%s:%s;%s:%s' % ( self.cookie_names['sid'],
                #                             self.session.cookies[self.cookie_names['sid']],
                #                             self.cookie_names['csrf'],
                #                             self.session.cookies[self.cookie_names['csrf']]),
                'X-CSRFToken': self.session.cookies[self.cookie_names['csrf']],
            }
            # print(headers)
            # Todo backend won't accept the request without csrf_exempt. Need to work on that
            response = super(SMDC, self).fetch(self.api_url + 'query/', method='POST',
                                               headers=headers, payload=json.dumps(query))
            self._print_json_response(response)
            df = self._json_2_dataframe(response)
            return df

        except (AccessDenied, MethodNotSupported) as e:
            raise

    def _print_json_response(self, response):
        r = json.loads(response)
        self.logger.debug(r)
        for elem in r['data']:
            self.logger.debug('request: %s' % elem['request'])
            self.logger.debug('code: %r' % elem['result']['code'])
            self.logger.debug('response array shape: (' + ','.join(map(lambda l: str(len(l)), elem['response'])) + ')')

    def _json_2_dataframe(self, json_obj, merge=True, normalize=True):
        """Converting the serialized JSON response from the back-end to Pandas DataFrame

        Args:
          jobj (dict or string): a JSON object (dict) or JSON encoded string
          merge (boolean): If merge is True, all series from the jobj will be merged into a single DataFrame.
            If different series have different timestamps, all timestamps will be merged into a single series of timestamps.
          normalize (boolean): If normalize is True, all timestamps will be normalized to the nearest time unit.

        Returns:
          a Pandas Data Frame or a list of Pandas Data Frames. None - when an error occurs.
        """
        if json_obj is None:
            return None

        if isinstance(json_obj, six.string_types):
            jobj = json.loads(json_obj)

        dfs = []
        try:
            for series in jobj['data']:
                if series['result']['code'] != 0:
                    df = pandas.DataFrame()
                    self.logger.warning('Provider returned an error response')
                elif len(series['response'][0]) == 0:
                    df = pandas.DataFrame()
                else:
                    data = {'dt': series['response'][0]}
                    for i in range(1, len(series['response'])):
                        data[series['request']] = series['response'][i]
                    df = pandas.DataFrame(data=data).set_index('dt')
                    if isinstance(df.index[0], str):
                        df.index = pandas.to_datetime(df.index)
                    else:
                        df.index = pandas.to_datetime(df.index, unit='s')
                dfs.append(df)
            if len(dfs) == 1:
                return dfs[0]
            return dfs
        except Exception as e:
            self.logger.error('Error converting JSON response to Pandas Data Frame')
            self.logger.error(e)
            self.logger.debug(traceback.format_exc())
            return None

    def _form_query(self, source, instrument, channel, start_dt, end_dt, time_frame, level='default'):
        """Forming a query according to the syntax of SMDC REST API

        Returns:
          dict: a dictionary that contains the query

        Raises:
          SatelliteNotFound:
          InstrumentNotFound:
          ChannelNotFound:
          ResponseSizeTooLarge:
          DateRangeTooLarge:
          TimeFrameTooSmall:
          TimeFrameNotAvailable:
        """
        if not self._is_source_available(source):
            self.logger.error('The provider has no such data source: %s' % source)
            raise SatelliteNotFound('The provider has no such data source: %s' % source)

        if not self._is_instrument_available(instrument, source):
            self.logger.error('The data source has no such instrument: %s' % instrument)
            raise SatelliteNotFound('The data source has no such instrument: %s' % instrument)

        if not self._is_channel_available(channel, instrument, source):
            self.logger.error('The instrument has no such data channel: %s' % channel)
            raise SatelliteNotFound('The instrument has no such data channel: %s' % channel)

        if not self._is_time_frame_available(time_frame, channel, instrument, source):
            self.logger.error('There is no data with such time frame: %s' % time_frame)
            raise SatelliteNotFound('There is no data with such time frame: %s' % time_frame)

        try:
            datetime.strptime(start_dt, dt_format)
        except ValueError:
            self.logger.error('Invalid start_dt: %s' % start_dt)
            raise DatetimeValueError('Invalid start_dt: %s' % start_dt)

        try:
            datetime.strptime(end_dt, dt_format)
        except ValueError:
            self.logger.error('Invalid end_dt: %s' % end_dt)
            raise DatetimeValueError('Invalid end_dt: %s' % end_dt)

        query = {
            "where": {
                "resolution": time_frame,
                "min_dt": start_dt,
                "max_dt": end_dt,
            },
            "select": [
                self._resolve_source(source) + '.' + instrument + '.' + channel,
            ]
        }
        if level != 'default':
            query['options'] = {'level': 'level2'}
        # self.logger.debug('Formed query: %s' % query)
        return query

    def _is_source_available(self, source):
        """Checking if the source is provided by the provider

        Returns:
          boolean: True if the provided source is available. False otherwise.
        TODO:
          fetch and cache the meta-data from the provider to search through it
          instead of sending a GET request each time
        """
        return True

    def _is_instrument_available(self, instrument, source):
        """Checking if the instrument is provided by the provider

        Returns:
          boolean: True if the provided instrument is available. False otherwise.
        TODO:
          fetch and cache the meta-data from the provider to search through it
          instead of sending a GET request each time
        """
        return True

    def _is_channel_available(self, channel, instrument, source):
        """Checking if channel is provided by the provider

        Returns:
          boolean: True if the provided channel is available. False otherwise.
        TODO:
          fetch and cache the meta-data from the provider to search through it
          instead of sending a GET request each time
        """
        return True

    def _is_time_frame_available(self, time_frame, channel, instrument, source):
        """Checking if time_frame is provided by the provider

        Returns:
          boolean: True if the provided time_frame is available. False otherwise.
        TODO:
          fetch and cache the meta-data from the provider to search through it
          instead of sending a GET request each time
        """
        return True

    def _resolve_source(self, source):
        if source in satellite_2_noradid:
            return str(satellite_2_noradid[source])
        else:
            return source


class ForecastModel(SMDC):
    def get_solar_wind_forecast(self, wave_length, start_dt, end_dt):
        source = 'sdo'
        if wave_length not in [193, 211, '193', '211', '0193', '0211']:
            raise ArgumentValueError('Invalid wave length. Possible values are 193 or 211')

        if isinstance(wave_length, int) and wave_length in [193, 211] or wave_length in ['193', '211']:
            wave_length = '0' + str(wave_length)

        instrument = 'sw_forecast_' + wave_length
        channel = 'forecast_sw_speed'
        return self.fetch(source=source,
                          instrument=instrument,
                          channel=channel,
                          start_dt=start_dt,
                          end_dt=end_dt,
                          time_frame='auto')
