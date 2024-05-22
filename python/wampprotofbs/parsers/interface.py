from flatbuffers import Builder, Table

from wampproto.messages import Hello, Message


class IMessageFBS:
    @staticmethod
    def from_fbs(msg: Table) -> Message:
        raise NotImplementedError

    @staticmethod
    def to_fbs(hello: Hello, builder: Builder):
        raise NotImplementedError
