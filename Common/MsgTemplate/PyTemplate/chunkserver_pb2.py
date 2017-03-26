# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chunkserver.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import response_pb2 as response__pb2
import request_pb2 as request__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='chunkserver.proto',
  package='perfuse',
  syntax='proto2',
  serialized_pb=_b('\n\x11\x63hunkserver.proto\x12\x07perfuse\x1a\x0eresponse.proto\x1a\rrequest.proto2C\n\x0b\x43hunkServer\x12\x34\n\x0bGetResponse\x12\x10.perfuse.Request\x1a\x11.perfuse.Response\"\x00')
  ,
  dependencies=[response__pb2.DESCRIPTOR,request__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)





try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces


  class ChunkServerStub(object):

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.GetResponse = channel.unary_unary(
          '/perfuse.ChunkServer/GetResponse',
          request_serializer=request__pb2.Request.SerializeToString,
          response_deserializer=response__pb2.Response.FromString,
          )


  class ChunkServerServicer(object):

    def GetResponse(self, request, context):
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_ChunkServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'GetResponse': grpc.unary_unary_rpc_method_handler(
            servicer.GetResponse,
            request_deserializer=request__pb2.Request.FromString,
            response_serializer=response__pb2.Response.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'perfuse.ChunkServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaChunkServerServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    def GetResponse(self, request, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaChunkServerStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    def GetResponse(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    GetResponse.future = None


  def beta_create_ChunkServer_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('perfuse.ChunkServer', 'GetResponse'): request__pb2.Request.FromString,
    }
    response_serializers = {
      ('perfuse.ChunkServer', 'GetResponse'): response__pb2.Response.SerializeToString,
    }
    method_implementations = {
      ('perfuse.ChunkServer', 'GetResponse'): face_utilities.unary_unary_inline(servicer.GetResponse),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_ChunkServer_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('perfuse.ChunkServer', 'GetResponse'): request__pb2.Request.SerializeToString,
    }
    response_deserializers = {
      ('perfuse.ChunkServer', 'GetResponse'): response__pb2.Response.FromString,
    }
    cardinalities = {
      'GetResponse': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'perfuse.ChunkServer', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
