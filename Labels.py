import struct

# Trb FileSize
class TSFL:
    def __init__(self, signature, size):
        self.signature = signature
        self.size = size
# IDK
class TRBF:
    def __init__(self, signature):
        self.signature = signature
# Information on Files
class HDRX:
    class File:
        def __init__(self, unknown, unknown2, fileSize, zero, flag):
            self.unknown = unknown
            self.unknown2 = unknown2
            self.fileSize = fileSize
            self.zero = zero
            self.flag = flag
    def __init__(self, signature, size, flag1, flag2, fileCount):
        self.signature = signature
        self.size = size
        self.flag1 = flag1
        self.flag2 = flag2
        self.fileCount = fileCount
        self.files = []
# This contains all files
class SECT:
    def __init__(self, signature, size):
        self.signature = signature
        self.size = size
# IDK
class RELC:
    def __init__(self, signature, size):
        self.signature = signature
        self.size = size
# Relocation Table
class SYMB:
    class Symbol:
        def __init__(self, name, Id, nameOffset, nameId, dataOffset):
            self.name = name
            self.Id = Id
            self.nameOffset = nameOffset
            self.nameId = nameId
            self.dataOffset = dataOffset
    def __init__(self, signature, size, symbolCount):
        self.signature = signature
        self.size = size
        self.symbolCount = symbolCount
        self.symbols = []
# Toshi Model
class TMOD:
    def __init__(self, header):
        self.header = header
    class Header:
        def __init__(self, modelFileNameOffset, modelCount, unknown, unknown1, vertexStride, referenceTomeshInfoOffsetBegin, meshInfoOffsetOffset, meshInfoOffset):
            self.modelFileNameOffset = modelFileNameOffset
            self.modelCount = modelCount
            self.unknown = unknown
            self.unknown1 = unknown1
            self.vertexStride = vertexStride
            self.referenceTomeshInfoOffsetBegin = referenceTomeshInfoOffsetBegin
            self.meshInfoOffsetOffset = meshInfoOffsetOffset
            self.meshInfoOffset = meshInfoOffset 
