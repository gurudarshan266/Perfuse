# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: response.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import defines_pb2 as defines__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='response.proto',
  package='perfuse',
  syntax='proto2',
  serialized_pb=_b('\n\x0eresponse.proto\x12\x07perfuse\x1a\rdefines.proto\"\x91\x01\n\x08Response\x12(\n\x06method\x18\x01 \x02(\x0e\x32\x13.perfuse.MethodType:\x03NOP\x12\x0e\n\x06respid\x18\x02 \x02(\x05\x12#\n\x08\x66ileinfo\x18\x03 \x01(\x0b\x32\x11.perfuse.FileInfo\x12&\n\nchunksinfo\x18\x04 \x03(\x0b\x32\x12.perfuse.ChunkInfo')
  ,
  dependencies=[defines__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='perfuse.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method', full_name='perfuse.Response.method', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=True, default_value=4,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='respid', full_name='perfuse.Response.respid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fileinfo', full_name='perfuse.Response.fileinfo', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chunksinfo', full_name='perfuse.Response.chunksinfo', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=43,
  serialized_end=188,
)

_RESPONSE.fields_by_name['method'].enum_type = defines__pb2._METHODTYPE
_RESPONSE.fields_by_name['fileinfo'].message_type = defines__pb2._FILEINFO
_RESPONSE.fields_by_name['chunksinfo'].message_type = defines__pb2._CHUNKINFO
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'response_pb2'
  # @@protoc_insertion_point(class_scope:perfuse.Response)
  ))
_sym_db.RegisterMessage(Response)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)