#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2018 Minh Duc Nguyen <bsd@conqueror.pro>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------

class BaseError(Exception):
    """The Base Error class for all exceptions"""
    pass

class ProviderNotSupported(BaseError):
    """The provider is not available or not supported"""
    pass

class AuthenticationError(BaseError):
    """The provided authentication credentials are invalid"""
    pass

class RequestTimeout(BaseError):
    """The data provider is not responding"""
    pass

class AccessDenied(BaseError):
    """The data provider does not allow accessing its data"""
    pass

class MethodNotSupported(BaseError):
    """The request method is not supported"""
    pass

class LocalNetworkError(BaseError):
    """Problems with local machine network connection"""
    pass

class SatelliteNotFound(BaseError):
    """There is no such satellite provided by the data provider"""
    pass

class InstrumentNotFound(BaseError):
    """The satellite has no such instrument"""
    pass

class ChannelNotFound(BaseError):
    """The instrument has no such data channel"""
    pass

class ResponseSizeTooLarge(BaseError):
    """The response size is too large to be passed through the Internet"""
    pass

class DateRangeTooLarge(BaseError):
    """The selected date time period is too large"""
    pass

class TimeFrameTooSmall(BaseError):
    """The data provider provide no data with such resolution or the selected resolution leads to a big response size"""
    pass

class TimeFrameNotAvailable(BaseError):
    """The data channel does not have data for this time frame"""
    pass

class DatetimeValueError(BaseError):
    """Invalid datetime value"""
    pass

class ArgumentValueError(BaseError):
    """Invalid argument value"""
    pass

class AuthConfigNotFound(BaseError):
    """Authentication configuration file not found"""
    pass

class AuthCredentialsNotFound(BaseError):
    """Authentication configuration file not found"""
    pass

# =============================================================================
