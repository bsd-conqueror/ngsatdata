#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import providers
import unittest
import pandas
class TestSmdcProvider(unittest.TestCase):
  def authorize(self):
    smdc = providers.smdc()
    self.assertEqual(smdc.authorize(), True)
    
  def form_query_default_level(self):
    smdc = providers.smdc()
    self.assertEqual(
      smdc._form_query(
        source='goes13',
        instrument='pchan',
        channel='p1',
        start_dt='2016-01-01 00:00:00',
        end_dt='2016-01-01 01:00:00',
        time_frame='5m'
        ),
      {
        'where': {
          'resolution': '5m',
          'min_dt': '2016-01-01 00:00:00',
          'max_dt': '2016-01-01 01:00:00',
        },
        'select': [
          '29155.pchan.p1'
        ]
      }
      )
  def fetch_goes13(self):
    smdc = providers.smdc()
    smdc.authorize()
    df = smdc.fetch(source='goes13',
                    instrument='pchan',
                    channel='p1',
                    start_dt='2016-01-01 00:00:00',
                    end_dt='2016-01-01 01:00:00',
                    time_frame='5m',
                    level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def fetch_electro_l2(self):
    smdc = providers.smdc()
    smdc.authorize()
    df = smdc.fetch(source='electro_l2',
                    instrument='skl',
                    channel='das3vrt1',
                    start_dt='2017-10-14 10:43:38',
                    end_dt='2017-10-14 10:43:47',
                    time_frame='1s',
                    level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)
    
  def get_solar_wind_forecast(self):
    from providers.smdc import models
    m = models()
    df = m.get_solar_wind_forecast(wave_length=193,
                                  start_dt='2017-10-14 10:00:00',
                                  end_dt='2017-10-14 12:00:00')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)
  def get_rss_ace_at_earth_density(self):
    smdc = providers.smdc()
    smdc.authorize()
    df = smdc.fetch(source='rss', instrument='ace_at_earth', channel='density',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def get_dst_index(self):
    import logging
    smdc = providers.smdc(log_level=logging.DEBUG)
    smdc.authorize()
    df = smdc.fetch(source='index', instrument='dst', channel='dst',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def get_goes_level2_e20_with_level(self):
    import logging
    smdc = providers.smdc(log_level=logging.DEBUG)
    smdc.authorize()
    df = smdc.fetch(source='goes15', instrument='e13ew_e2', channel='e2',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='1h', level='level2')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def get_goes_level2_e20_with_source_name(self):
    import logging
    smdc = providers.smdc(log_level=logging.DEBUG)
    smdc.authorize()
    df = smdc.fetch(source='goes15_level2', instrument='e13ew_e2', channel='e2',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='1h', level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def get_index_wolf(self):
    import logging
    smdc = providers.smdc(log_level=logging.DEBUG)
    smdc.authorize()
    df = smdc.fetch(source='index', instrument='wolf', channel='wolfnumber',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def get_meteor_m2_das4vrt7(self):
    import logging
    smdc = providers.smdc(log_level=logging.DEBUG)
    smdc.authorize()
    df = smdc.fetch(source='meteor_m2', instrument='skl1', channel='das4vrt7',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='1h', level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

  def get_electro_l2_das3vrt6(self):
    import logging
    smdc = providers.smdc(log_level=logging.DEBUG)
    smdc.authorize()
    df = smdc.fetch(source='electro_l2', instrument='skl', channel='das3vrt6',
                                  start_dt='2018-03-24 08:00:00',
                                  end_dt='2018-03-24 09:00:00', time_frame='1h', level='default')
    self.assertEqual(isinstance(df, pandas.DataFrame), True)

if __name__ == '__main__':
  # unittest.main()
  suite = unittest.TestLoader().loadTestsFromTestCase(TestSmdcProvider)
  unittest.TextTestRunner(verbosity=2).run(suite)
  # obj = providers.smdc()
  # obj.authorize()
  # dfs = obj.fetch('http://localhost:8000/db_iface/api/v2/query/', method='POST', payload="""{
  #     "where": {
  #       "resolution":"10m",
  #       "min_dt":"2014-06-06 00:00:00",
  #       "max_dt":"2014-06-06 00:59:59"
  #       },
  #       "options": {"unformated":"true"},
  #       "select": [
  #         "coord.meteor_m1_coord_10m.l",
  #         "35865.skl.das1vrt1",
  #         "35865.skl.das1vrt2",
  #         "35865.skl.das1vrt3"
  #      ]
  #   }"""
  #   )
  # if isinstance(dfs, list):
  #   for df in dfs:
  #     print(df)
  # else:
  #   print(dfs)
