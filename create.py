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

    Message.Start(builder)
    Message.AddMessage(builder, end)
    Message.AddMessageType(builder, Messages.Messages.Hello)
    end = Message.End(builder)
    builder.Finish(end)

    return builder.Output()


def create_welcome(session_id: int, authrole: str) -> bytearray:
    builder = Builder(1024)
    authrole = builder.CreateString(authrole)

    Welcome.Start(builder)
    Welcome.AddSessionId(builder, session_id)
    Welcome.AddAuthrole(builder, authrole)
    end = Welcome.End(builder)

    Message.Start(builder)
    Message.AddMessageType(builder, Messages.Messages.Welcome)
    Message.AddMessage(builder, end)
    end = Message.End(builder)
    builder.Finish(end)

    return builder.Output()


def main():
    hello_data = create_hello("realm1", "authid1", ["ticket"], "auth_provider")
    welcome_data = create_welcome(1 << 53, "authrole1")

    for data in [hello_data, welcome_data]:
        message = Message.Message.GetRootAs(data)
        table = message.Message()
        if message.MessageType() == Messages.Messages.Welcome:
            welcome = Welcome.Welcome.GetRootAs(table.Bytes)
            print("WELCOME", welcome.SessionId(), welcome.Authrole())
        elif message.MessageType() == Messages.Messages.Hello:
            hello = Hello.Hello.GetRootAs(table.Bytes)
            print("HELLO", hello.AuthmethodsLength(), hello.Authid())



if __name__ == "__main__":
    main()
