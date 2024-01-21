import logging
from dataclasses import dataclass
import boto3

from components.event_manager.event_manager import EventManager
from components.event_manager.event_body import EventBody


@dataclass
class EventManagerSNS(EventManager):

    def __init__(self, region_name, topic_arn):
        self.sns_client = boto3.client('sns', region_name=region_name)
        self.topic_arn = topic_arn

    def publish(self, body: EventBody):
        response = self.sns_client.publish(
            TopicArn=self.topic_arn,
            Message=body.data
        )
        logging.info(f"publish response: {response}")

    def consume(self, callback):
        raise NotImplementedError
