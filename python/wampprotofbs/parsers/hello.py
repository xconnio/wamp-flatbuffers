from flatbuffers import Builder, Table

from wampproto.messages import Hello, Message
from wampprotofbs.parsers.helpers import union
from wampprotofbs.parsers.interface import IMessageFBS
from wampprotofbs.gen import (
    Hello as HelloFBS,
    Messages as MessagesFBS,
)


class HelloParser(IMessageFBS):
    @staticmethod
    def from_fbs(msg: Table) -> Message:
        raise NotImplementedError

    @staticmethod
    def to_fbs(hello: Hello, builder: Builder):
        realm = builder.CreateString(hello.realm)
        authid = builder.CreateString(hello.authid)
        auth_provider = builder.CreateString("static")

        data = [builder.CreateString(string) for string in hello.authmethods]
        HelloFBS.StartAuthmethodsVector(builder, len(data))
        for item in data:
            builder.PrependSOffsetTRelative(item)

        methods = builder.EndVector()

        HelloFBS.Start(builder)
        HelloFBS.AddRealm(builder, realm)
        HelloFBS.AddAuthid(builder, authid)
        HelloFBS.AddAuthprovider(builder, auth_provider)
        HelloFBS.AddAuthmethods(builder, methods)

        end = HelloFBS.End(builder)
        builder.Finish(end)

        msg_bytes = builder.Output()
        builder.Clear()

        union(builder, msg_bytes, MessagesFBS.Messages.Hello)

        msg_bytes = builder.Output()
        builder.Clear()
        return msg_bytes
