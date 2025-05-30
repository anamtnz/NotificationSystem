from logging import Logger
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.routers.subscriber.subscriber import register, unregister
from app.subscriber.models import SubscriberAlreadyExistsException, SubscriberDoesNotExistsException

from test_app.conftest import subscriber_info_mock, subscriber_mock, subscriber_manager_mock, ID

TESTED_MODULE = 'app.routers.subscriber.subscriber'


@pytest.fixture
def subscriber_mock_initialized(subscriber_mock):
    subscriber_mock.id = ID
    subscriber_mock.name = 'test'
    subscriber_mock.url = 'https://test.com'


@patch(TESTED_MODULE + '._to_subscriber')
@patch(TESTED_MODULE + '.manager')
def test_register(manager_mock, _to_subscriber_mock, subscriber_info_mock, subscriber_mock_initialized,
                  subscriber_manager_mock):
    _to_subscriber_mock.return_value = subscriber_mock_initialized
    manager_mock.return_value = subscriber_manager_mock

    register(subscriber_info_mock)

    _to_subscriber_mock.assert_called_with(subscriber_info_mock)
    manager_mock.register.assert_called_with(subscriber_mock_initialized)


@patch(TESTED_MODULE + '._to_subscriber')
@patch(TESTED_MODULE + '.manager')
@patch.object(Logger, 'exception')
def test_register_subscriber_already_exists(exception_mock, manager_mock, _to_subscriber_mock, subscriber_info_mock,
                                            subscriber_mock_initialized, subscriber_manager_mock):
    _to_subscriber_mock.return_value = subscriber_mock_initialized
    manager_mock.return_value = subscriber_manager_mock
    manager_mock.register.side_effect = SubscriberAlreadyExistsException(ID)

    with pytest.raises(HTTPException) as e:
        register(subscriber_info_mock)

    assert e.value.status_code == 400
    assert e.value.detail == f"Subscriber {ID} already exists"
    _to_subscriber_mock.assert_called_with(subscriber_info_mock)
    manager_mock.register.assert_called_with(subscriber_mock_initialized)
    exception_mock.assert_called_once()


@patch(TESTED_MODULE + '._to_subscriber')
@patch(TESTED_MODULE + '.manager')
@patch.object(Logger, 'exception')
def test_register_exception(exception_mock, manager_mock, _to_subscriber_mock, subscriber_info_mock,
                            subscriber_mock_initialized, subscriber_manager_mock):
    _to_subscriber_mock.return_value = subscriber_mock_initialized
    manager_mock.return_value = subscriber_manager_mock
    manager_mock.register.side_effect = Exception

    with pytest.raises(HTTPException) as e:
        register(subscriber_info_mock)

    assert e.value.status_code == 500
    _to_subscriber_mock.assert_called_with(subscriber_info_mock)
    manager_mock.register.assert_called_with(subscriber_mock_initialized)
    exception_mock.assert_called_once()


@patch(TESTED_MODULE + '.manager')
def test_unregister(manager_mock, subscriber_manager_mock):
    manager_mock.return_value = subscriber_manager_mock

    unregister(ID)

    manager_mock.unregister.assert_called_with(ID)


@patch(TESTED_MODULE + '.manager')
@patch.object(Logger, 'exception')
def test_unregister_subscriber_does_not_exist(exception_mock, manager_mock, subscriber_manager_mock):
    manager_mock.return_value = subscriber_manager_mock
    manager_mock.unregister.side_effect = SubscriberDoesNotExistsException(ID)

    with pytest.raises(HTTPException) as e:
        unregister(ID)

    assert e.value.status_code == 400
    assert e.value.detail == f"Subscriber {ID} does not exist"
    manager_mock.unregister.assert_called_with(ID)
    exception_mock.assert_called_once()


@patch(TESTED_MODULE + '.manager')
@patch.object(Logger, 'exception')
def test_unregister_exception(exception_mock, manager_mock, subscriber_manager_mock):
    manager_mock.return_value = subscriber_manager_mock
    manager_mock.unregister.side_effect = Exception

    with pytest.raises(HTTPException) as e:
        unregister(ID)

    assert e.value.status_code == 500
    manager_mock.unregister.assert_called_with(ID)
    exception_mock.assert_called_once()