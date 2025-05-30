from unittest.mock import Mock

import pytest

from app.publisher.models import Notification
from app.publisher.publisher_manager import PublisherManager
from app.routers.publisher.models import NotificationInfo
from app.routers.subscriber.models import SubscriberInfo
from app.subscriber.models import Subscriber
from app.subscriber.subscriber_manager import SubscriberManager

ID = '0a639844-f3a3-4838-9f31-e04e4823a177'


@pytest.fixture
def publisher_manager_mock() -> Mock:
    return Mock(spec=PublisherManager)


@pytest.fixture
def subscriber_manager_mock() -> Mock:
    return Mock(spec=SubscriberManager)


@pytest.fixture
def subscriber_mock() -> Mock:
    return Mock(spec=Subscriber)


@pytest.fixture
def subscriber_info_mock() -> Mock:
    return Mock(spec=SubscriberInfo)


@pytest.fixture
def notification_mock() -> Mock:
    return Mock(spec=Notification)


@pytest.fixture
def notification_info_mock() -> Mock:
    return Mock(spec=NotificationInfo)
