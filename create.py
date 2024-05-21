from flatbuffers.builder import Builder

from wampproto import Hello, Welcome, Message, Messages


def create_hello(realm: str, authid: str, auth_methods: list[str], auth_provider: str = "static") -> bytearray:
    builder = Builder(1024)
    realm = builder.CreateString(realm)
    authid = builder.CreateString(authid)
    auth_provider = builder.CreateString(auth_provider)

    data = [builder.CreateString(string) for string in auth_methods]
    Hello.StartAuthmethodsVector(builder, len(auth_methods))
    for item in data:
        builder.PrependSOffsetTRelative(item)

    methods = builder.EndVector()

    Hello.Start(builder)
    Hello.AddRealm(builder, realm)
    Hello.AddAuthid(builder, authid)
    Hello.AddAuthprovider(builder, auth_provider)
    Hello.AddAuthmethods(builder, methods)

    end = Hello.End(builder)
    builder.Finish(end)

    byte_data = builder.Output()
    builder.Clear()

    return union(builder, byte_data, Messages.Messages.Hello)


def create_welcome(session_id: int, authrole: str) -> bytearray:
    builder = Builder(1024)
    authrole = builder.CreateString(authrole)

    Welcome.Start(builder)
    Welcome.AddAuthrole(builder, authrole)
    Welcome.AddSessionId(builder, session_id)
    welcome = Welcome.End(builder)
    builder.Finish(welcome)

    byte_data = builder.Output()
    builder.Clear()

    return union(builder, byte_data, Messages.Messages.Welcome)


def union(builder: Builder, msg_bytes: bytearray, message_type: int):
    byte_vector_offset = builder.CreateByteVector(msg_bytes)

    Message.Start(builder)
    Message.AddMessageType(builder, message_type)
    Message.AddMessage(builder, byte_vector_offset)
    end = Message.End(builder)
    builder.Finish(end)

    byte_data = builder.Output()
    builder.Clear()
    return byte_data


def main():
    hello_data = create_hello("realm1", "authid1", ["ticket"], "auth_provider")
    welcome_data = create_welcome(1 << 53, "authrole")

    for data in [welcome_data, hello_data]:
        message = Message.Message.GetRootAs(data)
        if message.MessageType() == Messages.Messages.Welcome:
            table = message.Message()
            welcome = Welcome.Welcome.GetRootAs(table.Bytes, table.Pos + 4)
            print("WELCOME", welcome.SessionId(), welcome.Authrole())
        elif message.MessageType() == Messages.Messages.Hello:
            table = message.Message()
            hello = Hello.Hello.GetRootAs(table.Bytes, table.Pos + 4)
            print("HELLO", hello.Authid(), hello.Realm(), hello.AuthmethodsIsNone(), hello.Authprovider())


if __name__ == "__main__":
    main()
