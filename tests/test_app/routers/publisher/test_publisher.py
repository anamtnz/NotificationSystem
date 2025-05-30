from logging import Logger
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.publisher.models import Notification
from app.routers.publisher.publisher import get_subscribers, send_notification, _to_notification
from test_app.conftest import publisher_manager_mock, subscriber_mock

TESTED_MODULE = 'app.routers.publisher.publisher'
SUBSCRIBERS = [subscriber_mock]


@patch(TESTED_MODULE + '.manager')
def test_get_subscribers(manager_mock, publisher_manager_mock):
    manager_mock.return_value = publisher_manager_mock
    manager_mock.get_subscribers.return_value = SUBSCRIBERS

    subscribers = get_subscribers()

    assert subscribers == SUBSCRIBERS
    manager_mock.get_subscribers.assert_called_once()


@patch(TESTED_MODULE + '.manager')
@patch.object(Logger, 'exception')
def test_get_subscribers_exception(exception_mock, manager_mock, publisher_manager_mock):
    manager_mock.return_value = publisher_manager_mock
    manager_mock.get_subscribers.side_effect = Exception

    with pytest.raises(HTTPException) as ex:
        get_subscribers()

    assert ex.value.status_code == 500
    manager_mock.get_subscribers.assert_called_once()
    exception_mock.assert_called_once()


@patch(TESTED_MODULE + '._to_notification')
@patch(TESTED_MODULE + '.manager')
def test_send_notification(manager_mock, _to_notification_mock, publisher_manager_mock, notification_mock,
                           notification_info_mock):
    _to_notification_mock.return_value = notification_mock
    manager_mock.return_value = publisher_manager_mock
    manager_mock.send_notification.return_value = []

    subscribers_list = send_notification(notification_info_mock)

    assert subscribers_list == []
    manager_mock.send_notification.assert_called_once()
    _to_notification_mock.assert_called_with(notification_info_mock)


@patch(TESTED_MODULE + '._to_notification')
@patch(TESTED_MODULE + '.manager')
@patch.object(Logger, 'exception')
def test_send_notification_exception(exception_mock, manager_mock, _to_notification_mock, publisher_manager_mock,
                           notification_mock, notification_info_mock):
    _to_notification_mock.return_value = notification_mock
    manager_mock.return_value = publisher_manager_mock
    manager_mock.send_notification.side_effect = Exception

    with pytest.raises(HTTPException) as ex:
        send_notification(notification_info_mock)

    assert ex.value.status_code == 500
    manager_mock.send_notification.assert_called_once()
    _to_notification_mock.assert_called_with(notification_info_mock)
    exception_mock.assert_called_once()

@patch.object(Notification, 'model_validate')
def test__to_notification(model_validate_mock, notification_mock, notification_info_mock):
    model_validate_mock.return_value = notification_mock

    notification = _to_notification(notification_info_mock)

    assert notification == notification_mock
    model_validate_mock.assert_called_with(notification_info_mock.model_dump())
