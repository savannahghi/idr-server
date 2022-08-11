from abc import ABCMeta, abstractmethod


class AbstractEventPublisher(metaclass=ABCMeta):
    """Base class for publish events"""

    @abstractmethod
    def publish_event(self, topic_path: str, data: dict):
        ...


class AbstractEventSubscriber(metaclass=ABCMeta):
    """Base class for subscribe events"""

    @abstractmethod
    def subscribe_to_event(self, topic_path: str, callback):
        ...
