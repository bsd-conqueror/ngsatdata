#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import unittest

import pandas
import pytest

from satdata.providers.smdc import SMDC, ForecastModel


class TestSmdcProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.smdc = SMDC(log_level=logging.DEBUG)
        self.smdc.authorize()
        self.assertEqual(self.smdc.authorize(), True)

    def form_query_default_level(self):
        self.assertEqual(
            self.smdc._form_query(
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

    # @pytest.mark.skip
    def test_fetch_goes13(self):
        df = self.smdc.fetch(source='goes13',
                             instrument='pchan',
                             channel='p1',
                             start_dt='2016-01-01 00:00:00',
                             end_dt='2016-01-01 01:00:00',
                             time_frame='5m',
                             level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_fetch_electro_l2(self):
        df = self.smdc.fetch(source='electro_l2',
                             instrument='skl',
                             channel='das3vrt1',
                             start_dt='2017-10-14 10:43:38',
                             end_dt='2017-10-14 10:43:47',
                             time_frame='1s',
                             level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_solar_wind_forecast(self):
        m = ForecastModel()
        m.authorize()
        df = m.get_solar_wind_forecast(wave_length=193,
                                       start_dt='2017-10-14 10:00:00',
                                       end_dt='2017-10-14 12:00:00')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_rss_ace_at_earth_density(self):
        df = self.smdc.fetch(source='rss', instrument='ace_at_earth', channel='density',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_dst_index(self):
        df = self.smdc.fetch(source='index', instrument='dst', channel='dst',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_goes_level2_e20_with_level(self):
        df = self.smdc.fetch(source='goes15', instrument='e13ew_e2', channel='e2',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='1h', level='level2')
        print(df)
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_goes_level2_e20_with_source_name(self):
        df = self.smdc.fetch(source='goes15_level2', instrument='e13ew_e2', channel='e2',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='1h', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_index_wolf(self):
        df = self.smdc.fetch(source='index', instrument='wolf', channel='wolfnumber',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_meteor_m2_das4vrt7(self):
        df = self.smdc.fetch(source='meteor_m2', instrument='skl1', channel='das4vrt7',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='1h', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_electro_l2_das3vrt6(self):
        df = self.smdc.fetch(source='electro_l2', instrument='skl', channel='das3vrt6',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='1h', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_dst_forecast(self):
        df = self.smdc.fetch(source='forecast', instrument='model_dst_v01', channel='dst',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_fluence_forecast(self):
        df = self.smdc.fetch(source='forecast', instrument='model_fluence_1d', channel='e20',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_model_solar_wind_forecast(self):
        df = self.smdc.fetch(source='models', instrument='ch', channel='forecast_sw_speed_193p',
                             start_dt='2018-03-24 08:00:00',
                             end_dt='2018-03-24 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_goes15_e13ew_level2(self):
        df = self.smdc.fetch(source='goes15_level2', instrument='e13ew_e2', channel='e2',
                             start_dt='2020-03-16 08:00:00',
                             end_dt='2020-03-16 09:00:00', time_frame='auto', level='default')
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_goes16_e2(self):
        df = self.smdc.fetch(source='goes16', instrument='integral_electrons', channel='e_ge_2',
                             start_dt='2020-03-16 18:00:00',
                             end_dt='2020-03-16 19:00:00', time_frame='auto', level='default')
        print(df.head)
        self.assertEqual(isinstance(df, pandas.DataFrame), True)

    # @pytest.mark.skip
    def test_get_goes16_xray(self):
        df = self.smdc.fetch(source='goes16', instrument='xrays', channel='nm01_08',
                             start_dt='2020-03-16 18:00:00',
                             end_dt='2020-03-16 19:00:00', time_frame='auto', level='default')
        print(df.head)
        self.assertEqual(isinstance(df, pandas.DataFrame), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSmdcProvider)
    unittest.TextTestRunner(verbosity=2).run(suite)
