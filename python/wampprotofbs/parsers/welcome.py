from flatbuffers import Builder, Table

from wampproto.messages import Welcome, Message
from wampprotofbs.parsers.interface import IMessageFBS


class WelcomeParser(IMessageFBS):
    @staticmethod
    def from_fbs(msg: Table) -> Message:
        raise NotImplementedError

    @staticmethod
    def to_fbs(welcome: Welcome, builder: Builder):
        raise NotImplementedError
