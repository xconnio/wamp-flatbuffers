from flatbuffers import Builder

from wampprotofbs.gen import Message as MessageFBS


def union(builder: Builder, msg_bytes: bytearray, message_type: int):
    byte_vector_offset = builder.CreateByteVector(msg_bytes)

    MessageFBS.Start(builder)
    MessageFBS.AddMessageType(builder, message_type)
    MessageFBS.AddMessage(builder, byte_vector_offset)
    end = MessageFBS.End(builder)
    builder.Finish(end)
