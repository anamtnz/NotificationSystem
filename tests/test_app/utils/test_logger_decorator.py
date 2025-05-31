from logging import Logger
from unittest.mock import patch, call

import pytest

from app.utils.logger_decorator import logger_decorator


@patch.object(Logger, 'info')
@patch.object(Logger, 'exception')
def test_logger_decorator(exception_mock, info_mock):
    @logger_decorator
    def function_to_decorate():
        pass

    function_to_decorate()

    info_mock.assert_has_calls(
        [call("Starting function function_to_decorate. Args: (). Kwargs: {}"),
         call("Finishing function function_to_decorate. Args: (). Kwargs: {}")])
    exception_mock.assert_not_called()


@patch.object(Logger, 'info')
@patch.object(Logger, 'exception')
def test_logger_decorator_exception(exception_mock, info_mock):
    @logger_decorator
    def function_to_decorate():
        raise Exception

    with pytest.raises(Exception):
        function_to_decorate()

    info_mock.assert_has_calls(
        [call("Starting function function_to_decorate. Args: (). Kwargs: {}"),
         call("Finishing function function_to_decorate. Args: (). Kwargs: {}")])
    exception_mock.assert_called_once_with("Exception executing function function_to_decorate. Args: (). Kwargs: {}: ")
