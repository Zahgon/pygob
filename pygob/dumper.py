import io

from .types import (GoBool, GoInt, GoUint, GoFloat, GoStruct, GoByteSlice,
                    GoString, GoComplex)


class Dumper:
    def __init__(self):
        self.types = {
            bool: GoBool,
            int: GoInt,
            float: GoFloat,
            bytes: GoByteSlice,
            str: GoString,
            complex: GoComplex,
        }

    def dump(self, value):
        pass

    def _dump(self, value):
        # Top-level singletons are sent with an extra zero byte which
        # serves as a kind of field delta.
        pass
