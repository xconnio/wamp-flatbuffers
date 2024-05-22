from flatbuffers import Builder

from wampproto import messages, serializers

from wampprotofbs.parsers import (
    hello,
    welcome,
)
from wampprotofbs.gen import (
    Message,
    Messages,
)


class FlatBuffersSerializer(serializers.Serializer):
    def serialize(self, message: messages.Message) -> bytes:
        if isinstance(message, messages.Hello):
            builder = Builder(1024)
            return hello.to_fbs(message, builder)
        elif isinstance(message, messages.Welcome):
            builder = Builder(1024)
            return welcome.to_fbs(message, builder)
        else:
            raise TypeError("unknown message type")

    def deserialize(self, data: bytes) -> messages.Message:
        message = Message.Message.GetRootAs(data)
        table = message.Message()
        match message.MessageType():
            case Messages.Messages.Hello:
                return hello.from_fbs(table)
            case Messages.Messages.Welcome:
                return welcome.from_fbs(table)
            case _:
                raise ValueError("not supported.")
