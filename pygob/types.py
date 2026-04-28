"""The predefined gob types.

These are the well-known gob types that both senders and receivers
already agree on to bootstrap the protocol.
"""

import struct
import collections

# We do not use an Enum for this since this set isn't the full set of
# all type IDs -- the protocol allows a sender to define custom IDs in
# terms of the IDs below.
BOOL = 1
INT = 2
UINT = 3
FLOAT = 4
BYTE_SLICE = 5
STRING = 6
COMPLEX = 7
INTERFACE = 8
# gap for reserved ids.
WIRE_TYPE = 16
ARRAY_TYPE = 17
COMMON_TYPE = 18
SLICE_TYPE = 19
STRUCT_TYPE = 20
FIELD_TYPE = 21
FIELD_TYPE_SLICE = 22
MAP_TYPE = 23


class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class GoType:
    """Represents a Go type.

    Go types know how to decode a gob stream to their corresponding
    Python type.
    """
    pass


class GoBool(GoType):
    """An Go Boolean.

    Go Booleans are mapped to Python Booleans. This class is meant to
    be used statically.
    """
    typeid = BOOL
    zero = False

    @staticmethod
    def decode(buf):
        """Decode a Boolean from buf. Returns the Boolean and the remainder of
        the buffer:

        >>> GoBool.decode(bytes([0]))
        (False, b'')
        >>> GoBool.decode(bytes([1]))
        (True, b'')
        """
        pass

    @staticmethod
    def encode(b):
        """Encode a Python Boolean as a Go bool:

        >>> list(GoBool.encode(False))
        [0]
        >>> list(GoBool.encode(True))
        [1]
        """
        pass


class GoUint(GoType):
    """An unsigned Go integer.

    Go unsigned integers are mapped to Python integers. This class is
    meant to be used statically.
    """
    typeid = UINT
    zero = 0

    @staticmethod
    def decode(buf):
        """Decode an unsigned integer from buf. Returns the integer and the
        remainder of the buffer:

        >>> GoUint.decode(bytes([56]))
        (56, b'')
        >>> GoUint.decode(bytes([254, 1, 0]))
        (256, b'')
        """
        pass

    @staticmethod
    def encode(n):
        """Encode a Python integer as an unsigned Go int:

        >>> list(GoUint.encode(56))
        [56]
        >>> list(GoUint.encode(256))
        [254, 1, 0]
        """
        pass


class GoInt(GoType):
    """A signed Go integer.

    Go signed integers are mapped to Python integers. This class is
    meant to be used statically.
    """
    typeid = INT
    zero = 0

    @staticmethod
    def decode(buf):
        """Decode a signed integer from buf. Returns the integer and the
        remainder of the buffer:

        >>> GoInt.decode(bytes([5]))
        (-3, b'')
        >>> GoInt.decode(bytes([6]))
        (3, b'')
        """
        pass

    @staticmethod
    def encode(n):
        """Encode a Python integer as a signed Go int:

        >>> list(GoInt.encode(-3))
        [5]
        >>> list(GoInt.encode(3))
        [6]
        """
        pass


class GoFloat(GoType):
    """A Go 64-bit float.

    Go floats are mapped to Python floats. This class is meant to be
    used statically.
    """
    typeid = FLOAT
    zero = 0.0

    @staticmethod
    def decode(buf):
        """Decode a 64-bit floating point number from buf. Returns the float
        and the remainder of the buffer:

        >>> GoFloat.decode(bytes([0]))
        (0.0, b'')
        >>> GoFloat.decode(bytes([254, 244, 63]))
        (1.25, b'')
        """
        pass

    @staticmethod
    def encode(f):
        """Encode a Python floating point number as a Go float64:

        >>> list(GoFloat.encode(0.0))
        [0]
        >>> list(GoFloat.encode(1.25))
        [254, 244, 63]

        Interestingly, Python's representation of NaN (not a number)
        is different from Go's. Python uses:

        >>> list(struct.pack('d', float('nan')))
        [0, 0, 0, 0, 0, 0, 248, 127]

        whereas Go uses `[1, 0, 0, 0, 0, 0, 248, 127]`. However, both
        are valid ways of representing a IEEE 754 NaN value:

        >>> GoFloat.decode(bytes([248, 1, 0, 0, 0, 0, 0, 248, 127]))
        (nan, b'')
        >>> GoFloat.decode(bytes([254, 248, 127]))
        (nan, b'')

        They only differ in the so-called "payload" of the value,
        which is ignored in most applications.
        """
        pass


class GoByteSlice(GoType):
    """A Go byte slice.

    Go byte slices are mapped to Python bytearrays.

    This class is meant to be used statically.
    """
    typeid = BYTE_SLICE

    @classproperty
    def zero(cls):
        pass

    @staticmethod
    def decode(buf):
        """Decode a byte slice from buf. Returns the slice and the remainder
        of the buffer:

        >>> GoByteSlice.decode(bytes([5, 104, 101, 108, 108, 111]))
        (bytearray(b'hello'), b'')
        """
        pass

    @staticmethod
    def encode(buf):
        """Encode a Python bytes value as a Go byte slice:

        >>> list(GoByteSlice.encode(b'hello'))
        [5, 104, 101, 108, 108, 111]
        """
        pass


class GoString(GoType):
    """A Go string.

    Go strings are mapped to Python bytes since Go strings do not
    guarantee any particular encoding. This class is meant to be used
    statically.
    """
    typeid = STRING
    zero = b''

    @staticmethod
    def decode(buf):
        """Decode a string from buf. Since Go strings do not guarantee any
        particular encoding, the data is returned as bytes:

        >>> GoString.decode(bytes([5, 104, 101, 108, 108, 111]))
        (b'hello', b'')
        """
        pass

    @staticmethod
    def encode(s):
        """Encode a Python string as a Go string. The string will be UTF-8
        encoded before being turned into bytes since most Go programs
        will expect that encoding:

        >>> GoString.encode('alpha: α')
        b'\\talpha: \\xce\\xb1'
        """
        pass


class GoComplex(GoType):
    """A Go complex number.

    Go complex numbers are mapped to Python complex numbers. This
    class is meant to be used statically.
    """
    typeid = COMPLEX
    zero = 0 + 0j

    @staticmethod
    def decode(buf):
        """Decode a complex number from `buf`. Returns the number and the
        remainder of the buffer:

        >>> GoComplex.decode(bytes([0, 254, 244, 63]))
        (1.25j, b'')
        """
        pass

    @staticmethod
    def encode(z):
        """Encode a complex number:

        >>> list(GoComplex.encode(1.25j))
        [0, 254, 244, 63]
        """
        pass


class GoStruct(GoType):
    """A Go struct.

    Go structs are mapped to Python named tuples.
    """

    @property
    def zero(self):
        pass

    def __init__(self, typeid, name, loader, fields):
        """A Go struct with a certain set of fields.

        The zero value of a GoStruct is based on the zero values of
        each field:

        >>> from pygob import Loader
        >>> person = GoStruct(142, 'Person', Loader(), [
        ...     ('Name', STRING),
        ...     ('Age', INT),
        ... ])
        >>> person.zero
        Person(Name=b'', Age=0)
        """
        self.typeid = typeid
        self._name = name
        self._loader = loader
        self._fields = fields
        self._class = collections.namedtuple(name, [n for (n, t) in fields])

    def decode(self, buf):
        """Decode data from buf and return a namedtuple."""
        pass

    def __repr__(self):
        """GoStruct representation.

        >>> GoStruct(142, 'Person', None, [('Name', STRING), ('Age', INT)])
        <GoStruct Person Name=6, Age=2>
        """
        fields = ['%s=%s' % f for f in self._fields]
        return '<GoStruct %s %s>' % (self._name, ', '.join(fields))


class GoWireType(GoStruct):
    """A Go wire type.

    This type is used in the gob stream to describe custom types.
    Decoding a WIRE_TYPE value yields another GoType subclass which
    can be used later to decode actual values of the custom type.
    """

    def decode(self, buf):
        """Decode data from buf and return a GoType."""
        pass


class GoArray(GoType):
    """A Go array.

    Go arrays are mapped to Python tuples.
    """

    @property
    def zero(self):
        pass

    def __init__(self, typeid, loader, elem, length):
        """A Go array of a certain type and length.

        >>> from pygob import Loader
        >>> int3 = GoArray(142, Loader(), INT, 3)
        >>> int3.zero
        (0, 0, 0)
        """
        self.typeid = typeid
        self._loader = loader
        self._elem = elem
        self._length = length

    def decode(self, buf):
        """Decode data from buf and return a tuple.

        Go arrays have a fixed size and cannot be resized. This makes
        them more like Python tuples than Python lists.
        """
        pass


class GoSlice(GoType):
    """A Go slice.

    Go slices are mapped to Python lists.
    """

    @property
    def zero(cls):
        pass

    def __init__(self, typeid, loader, elem):
        """A Go slice of a certain type.

        >>> from pygob import Loader
        >>> int_slice = GoSlice(142, Loader(), INT)
        >>> int_slice.zero
        []
        """
        self.typeid = typeid
        self._loader = loader
        self._elem = elem

    def decode(self, buf):
        """Decode data from buf and return a list.

        Go slices can extended later (with a possible reallocation of
        the underlying array) and are thus similar to Python lists.
        """
        pass


class GoMap(GoType):
    """A Go map.

    Go maps are mapped to Python dictionaries.
    """

    @property
    def zero(cls):
        pass

    def __init__(self, typeid, loader, key_typeid, elem_typeid):
        """A Go map with a certain key and element type.

        >>> from pygob import Loader
        >>> int_string_map = GoMap(142, Loader(), INT, STRING)
        >>> int_string_map.zero
        {}
        """
        self.typeid = typeid
        self._loader = loader
        self._key_typeid = key_typeid
        self._elem_typeid = elem_typeid

    def decode(self, buf):
        """Decode data from buf and return a dict."""
        pass
