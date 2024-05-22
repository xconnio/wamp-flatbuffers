from flatbuffers import Builder, Table

from wampproto.messages import Welcome, Message


def from_fbs(msg: Table) -> Message:
    raise NotImplementedError


def to_fbs(welcome: Welcome, builder: Builder):
    raise NotImplementedError
