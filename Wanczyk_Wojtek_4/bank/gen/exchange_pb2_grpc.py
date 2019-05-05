# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import exchange_pb2 as exchange__pb2


class ExchangeStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.subscribeForExchange = channel.unary_stream(
        '/Exchange/subscribeForExchange',
        request_serializer=exchange__pb2.ExchangeRequest.SerializeToString,
        response_deserializer=exchange__pb2.ExchangeStream.FromString,
        )


class ExchangeServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def subscribeForExchange(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ExchangeServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'subscribeForExchange': grpc.unary_stream_rpc_method_handler(
          servicer.subscribeForExchange,
          request_deserializer=exchange__pb2.ExchangeRequest.FromString,
          response_serializer=exchange__pb2.ExchangeStream.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Exchange', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
