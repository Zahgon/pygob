from .types import (BOOL, INT, UINT, FLOAT, BYTE_SLICE, STRING, COMPLEX,
                    WIRE_TYPE, ARRAY_TYPE, COMMON_TYPE, SLICE_TYPE,
                    STRUCT_TYPE, FIELD_TYPE, FIELD_TYPE_SLICE, MAP_TYPE)
from .types import (GoBool, GoUint, GoInt, GoFloat, GoByteSlice, GoString,
                    GoComplex, GoStruct, GoWireType, GoSlice)


class Loader:
    def __init__(self):
        # Compound types that depend on the basic types above.
        common_type = GoStruct(COMMON_TYPE, 'CommonType', self, [
            ('Name', STRING),
            ('Id', INT),
        ])
        array_type = GoStruct(ARRAY_TYPE, 'ArrayType', self, [
            ('CommonType', COMMON_TYPE),
            ('Elem', INT),
            ('Len', INT),
        ])
        slice_type = GoStruct(SLICE_TYPE, 'SliceType', self, [
            ('CommonType', COMMON_TYPE),
            ('Elem', INT),
        ])
        struct_type = GoStruct(STRUCT_TYPE, 'StructType', self, [
            ('CommonType', COMMON_TYPE),
            ('Field', FIELD_TYPE_SLICE),
        ])
        field_type = GoStruct(FIELD_TYPE, 'FieldType', self, [
            ('Name', STRING),
            ('Id', INT),
        ])
        field_type_slice = GoSlice(FIELD_TYPE_SLICE, self, FIELD_TYPE)
        map_type = GoStruct(MAP_TYPE, 'MapType', self, [
            ('CommonType', COMMON_TYPE),
            ('Key', INT),
            ('Elem', INT),
        ])
        wire_type = GoWireType(WIRE_TYPE, 'WireType', self, [
            ('ArrayT', ARRAY_TYPE),
            ('SliceT', SLICE_TYPE),
            ('StructT', STRUCT_TYPE),
            ('MapT', MAP_TYPE),
        ])

        # We can now register basic and compound types.
        self.types = {
            INT: GoInt,
            UINT: GoUint,
            BOOL: GoBool,
            FLOAT: GoFloat,
            BYTE_SLICE: GoByteSlice,
            STRING: GoString,
            COMPLEX: GoComplex,
            WIRE_TYPE: wire_type,
            ARRAY_TYPE: array_type,
            COMMON_TYPE: common_type,
            SLICE_TYPE: slice_type,
            STRUCT_TYPE: struct_type,
            FIELD_TYPE: field_type,
            FIELD_TYPE_SLICE: field_type_slice,
            MAP_TYPE: map_type,
        }

    def load(self, buf):
        pass

    def load_all(self, buf):
        pass

    def _read_segment(self, buf):
        pass

    def _load(self, buf):
        pass

    def decode_value(self, typeid, buf):
        pass
