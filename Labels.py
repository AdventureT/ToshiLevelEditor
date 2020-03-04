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
        self.meshesInfo = None
        self.meshInfos = []
        self.meshSubInfos = []
    def __del__(self):
        self.header = None
        self.meshesInfo = None
        self.meshInfos = []
        self.meshSubInfos = []
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
    class MeshesInfo:
        def __init__(self, offsetToOne, meshInfoOffsetOffset, meshCount):
            self.offsetToOne = offsetToOne
            self.meshInfoOffsetOffset = meshInfoOffsetOffset
            self.meshCount = meshCount
            self.meshInfoOffsets = []
    class MeshInfo:
        def __init__(self, zero, one, unknown1, unknown2, meshNameOffset, meshSubInfoOffset):
            self.zero = zero
            self.one = one
            self.unknown1 = unknown1
            self.unknown2 = unknown2
            self.meshNameOffset = meshNameOffset
            self.meshSubInfoOffset = meshSubInfoOffset
    class MeshSubInfo:
        def __init__(self, vertexCount, normalCount, faceCount, one, offsetToAnotherOne, vertexOffset, faceOffset):
            self.vertexCount = vertexCount
            self.normalCount = normalCount
            self.faceCount = faceCount
            self.one = one
            self.offsetToAnotherOne = offsetToAnotherOne
            self.vertexOffset = vertexOffset
            self.faceOffset = faceOffset
class Terrain:
    def __init__(self, unknown, unknown1, unknownInfoOffset, countOfUnknownInfo, cellInfoOffset, unknownOffsetToList, cellInfoCount, unknownOffset3):
        self.unknown = unknown
        self.unknown1 = unknown1
        self.unknownInfoOffset = unknownInfoOffset
        self.countOfUnknownInfo = countOfUnknownInfo
        self.cellInfoOffset = cellInfoOffset
        self.unknownOffsetToList = unknownOffsetToList
        self.cellInfoCount = cellInfoCount
        self.unknownOffset3 = unknownOffset3
    # 64 bytes
    class UnknownInfo:
        def __init__(self, matrixOffset, unknownOffset2, typeNameOffset, modelNameOffset, matrixOffset2, padding, uvNameOffset, padding2, textureNamesOffsetOffset, padding3):
            self.matrixOffset = matrixOffset
            self.unknownOffset2 = unknownOffset2
            self.typeNameOffset = typeNameOffset
            self.modelNameOffset = modelNameOffset
            self.matrixOffset2 = matrixOffset2
            self.padding = padding # 12 bytes
            self.uvNameOffset = uvNameOffset
            self.padding2 = padding2 # 12 bytes
            self.textureNamesOffsetOffset = textureNamesOffsetOffset
            self.padding3 = padding3 # 12 bytes
    # 60 bytes
    class CellInfo:
        def __init__(self, cellNameOffset, floatsOffset, floatsOffset2, floatsOffset3, cellPathOffsetOffset, zero, zero1, matrixOffset, 
        unknown, unknown1, unknownInfoPointer, zero2, zero3, zero4, zero5):
            self.cellNameOffset = cellNameOffset
            self.floatsOffset = floatsOffset # 4 floats
            self.floatsOffset2 = floatsOffset2 # 4 floats last value 1
            self.floatsOffset3 = floatsOffset3 # 4 floats last value 1
            self.cellPathOffsetOffset = cellPathOffsetOffset
            self.zero = zero
            self.zero1 = zero1
            self.matrixOffset = matrixOffset
            self.unknown = unknown
            self.unknown1 = unknown1
            self.unknownInfoPointer = unknownInfoPointer # class UnknownInfo
            self.zero2 = zero2
            self.zero3 = zero3
            self.zero4 = zero4
            self.zero5 = zero5
#class LightingData:



