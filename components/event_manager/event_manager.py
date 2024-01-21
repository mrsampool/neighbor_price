from dataclasses import dataclass
from components.event_manager.event_body import EventBody

EVENT_QUEUE_MODE_RABBITMQ = "rabbitmq"
EVENT_QUEUE_MODE_SNS = "sns"

@dataclass
class EventManager:

    def publish(self, body: EventBody):
        raise NotImplementedError

    def consume(self, callback):
        raise NotImplementedError
