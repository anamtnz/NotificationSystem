from logging import Logger
from unittest.mock import patch, call

import pytest

from app.publisher.publisher_manager import PublisherManager
from app.subscriber.models import SubscriberAlreadyExistsException, SubscriberDoesNotExistsException
from test_app.conftest import ID, subscriber_mock

TESTED_MODULE = 'app.publisher.publisher_manager'


@pytest.fixture
def subscriber_mock_initialized(subscriber_mock):
    subscriber_mock.id = ID
    subscriber_mock.name = 'test'
    subscriber_mock.url = 'https://test.com'
    return subscriber_mock


class TestPublisherManager:
    @pytest.fixture
    def publisher_manager(self, ) -> PublisherManager:
        return PublisherManager()

    def test_add_subscriber(self, publisher_manager, subscriber_mock_initialized):
        publisher_manager.add_subscriber(subscriber_mock_initialized)

    def test_add_subscriber_already_exists(self, publisher_manager, subscriber_mock_initialized):
        publisher_manager._subscribers[ID] = subscriber_mock_initialized

        with pytest.raises(SubscriberAlreadyExistsException):
            publisher_manager.add_subscriber(subscriber_mock_initialized)

    def test_delete_subscriber(self, publisher_manager, subscriber_mock_initialized):
        publisher_manager._subscribers[ID] = subscriber_mock_initialized

        publisher_manager.delete_subscriber(ID)

    def test_delete_subscriber_does_not_exist(self, publisher_manager, subscriber_mock_initialized):
        publisher_manager._subscribers[ID] = subscriber_mock_initialized

        with pytest.raises(SubscriberDoesNotExistsException):
            publisher_manager.delete_subscriber(subscriber_mock_initialized)

    def test_get_subscribers(self, publisher_manager, subscriber_mock):
        publisher_manager._subscribers[ID] = subscriber_mock

        subscribers = publisher_manager.get_subscribers()

        assert subscribers == [subscriber_mock]

    @patch(TESTED_MODULE + '.PublisherManager.get_subscribers')
    @patch(TESTED_MODULE + '.post')
    @patch.object(Logger, 'exception')
    def test_send_notification(self, exception_mock, post_mock, get_subscribers_mock, publisher_manager,
                               notification_mock, subscriber_mock_initialized):
        get_subscribers_mock.return_value = [subscriber_mock_initialized]

        subscribers_not_notified = publisher_manager.send_notification(notification_mock)

        assert subscribers_not_notified == []
        get_subscribers_mock.assert_called_once()
        post_calls = []
        for subscriber in [subscriber_mock_initialized]:
            post_calls.append(call(subscriber.url, json=notification_mock.model_dump()))
        post_mock.assert_has_calls(post_calls)
        exception_mock.assert_not_called()

    @patch(TESTED_MODULE + '.PublisherManager.get_subscribers')
    @patch(TESTED_MODULE + '.post')
    @patch.object(Logger, 'exception')
    def test_send_notification_exception(self, exception_mock, post_mock, get_subscribers_mock, publisher_manager,
                                         notification_mock, subscriber_mock_initialized):
        get_subscribers_mock.return_value = [subscriber_mock_initialized]
        post_mock.side_effect = Exception

        subscribers_not_notified = publisher_manager.send_notification(notification_mock)

        assert subscribers_not_notified == [ID]
        post_calls = []
        exception_calls = []
        for subscriber in [subscriber_mock_initialized]:
            post_calls.append(call(subscriber.url, json=notification_mock.model_dump()))
            exception_calls.append(call(f"Error sending notification to subscriber {subscriber.id}: "))

        post_mock.assert_has_calls(post_calls)
        exception_mock.assert_has_calls(exception_calls)
