import json
from channels.generic.websocket import WebsocketConsumer
from .fitcore import grayscale

class ChannelTest(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        if text_data=="ping":
            self.send("pong")
        else:
            self.send(text_data)
