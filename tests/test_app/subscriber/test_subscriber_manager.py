import pytest

from app.subscriber.subscriber_manager import SubscriberManager
from test_app.conftest import publisher_manager_mock, subscriber_mock, ID


class TestSubscriberManager:
    @pytest.fixture
    def subscriber_manager(self, publisher_manager_mock) -> SubscriberManager:
        return SubscriberManager(publisher_manager_mock)

    def test_register(self, publisher_manager_mock, subscriber_mock, subscriber_manager):
        subscriber_manager.register(subscriber_mock)

        publisher_manager_mock.add_subscriber.assert_called_once_with(subscriber_mock)

    def test_unregister(self, publisher_manager_mock, subscriber_mock, subscriber_manager):
        subscriber_manager.unregister(ID)

        publisher_manager_mock.delete_subscriber.assert_called_once_with(ID)
