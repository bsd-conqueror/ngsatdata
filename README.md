# SatData - a Python library for fetch space weather datasets

SatData has a machine-learning-ready unified API that allows you to fetch all
public available space weather datasets of a data center via its provided
driver.
Currently, only one driver by the Space Monitoring Data Center (SMDC -
http://smdc.sinp.msu.ru) of SINP MSU is
provided.

If you're interested in using SatData in your work, please send me an e-mail to
nguyendmitri@gmail.com.

# Examples

## To use the SMDC driver

* create a file called smdc_config.json
* put it to the same folder where smdc.py is located
* add the following authorization credentials to smdc_config.json
```
{
  "username": "your SMDC username",
  "password": "you SMDC password"
}
```

