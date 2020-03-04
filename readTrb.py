import struct
from . Labels import *
from . FileHelper import *


def read(filepath, t):
    f = open(filepath, "rb")
    tsfl = TSFL(readString(f,4), readUInt(f))
    trbf = TRBF(readString(f,4))
    hdrx = HDRX(readString(f,4), readUInt(f), readUShort(f), readUShort(f), readUInt(f))
    for x in range(hdrx.fileCount):
        file = HDRX.File(readUShort(f), readUShort(f), readUInt(f), readUInt(f), readUInt(f))
        if (x != 0):
            file.fileSize += hdrx.files[x-1].fileSize
        hdrx.files.append(file)
    sect = SECT(readString(f,4), readUInt(f))
    chunk = f.tell()
    f.seek(sect.size,1)
    relc = RELC(readString(f,4), readUInt(f))
    f.seek(relc.size,1)
    symb = SYMB(readString(f,4), readUInt(f), readUInt(f))
    cur = f.tell()
    for x in range(symb.symbolCount):
        c = SYMB.Symbol("", readUShort(f), readUInt(f), readUShort(f), readUInt(f))
        cu = f.tell()
        f.seek(cur + (symb.symbolCount * 12) + c.nameOffset,0)
        c.name = readString(f)
        f.seek(cu,0)
        symb.symbols.append(c)
        print("SYMB ",x,": ", c.name)
    f.seek(chunk,0)
    baseChunk = chunk
    for x in range(len(symb.symbols)):
        if symb.symbols[x].Id is not 0:
            chunk = hdrx.files[symb.symbols[x].Id - 1].fileSize + baseChunk
        f.seek(chunk + symb.symbols[x].dataOffset, 0)
        if t is 0:
            if symb.symbols[x].name == "tmod":
                tell = f.tell()
                tmod = TMOD(TMOD.Header(readUInt(f), readUInt(f), readFloat(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)))
                f.seek(tmod.header.modelFileNameOffset + chunk, 0)
                modelName = readString(f)
                f.seek(tmod.header.meshInfoOffset + chunk, 0)
                tmod.meshesInfo = TMOD.MeshesInfo(readUInt(f), readUInt(f), readUInt(f))
                for y in range(tmod.meshesInfo.meshCount):
                    tmod.meshesInfo.meshInfoOffsets.append(readUInt(f))
                print("Mesh Count: ", tmod.meshesInfo.meshCount, "Model Name: ", modelName)
                for z in range(tmod.meshesInfo.meshCount):
                    f.seek(tmod.meshesInfo.meshInfoOffsets[z] + chunk, 0)
                    tmod.meshInfos.append(TMOD.MeshInfo(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)))
                    f.seek(tmod.meshInfos[z].meshNameOffset + chunk, 0)
                    meshName = readString(f)
                    print("\t Mesh Name: ", meshName)
                for j in range(tmod.meshesInfo.meshCount):
                    f.seek(tmod.meshInfos[j].meshSubInfoOffset + chunk, 0)
                    tmod.meshSubInfos.append(TMOD.MeshSubInfo(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)))
                    print("Vertices: ", tmod.meshSubInfos[j].vertexCount, " Faces: ", tmod.meshSubInfos[j].faceCount)
                for i in range(tmod.meshesInfo.meshCount):
                    f.seek(tmod.meshSubInfos[i].vertexOffset + chunk, 0)
                del tmod
        else:
            if symb.symbols[x].name == "Terrain_Main":
                tell = f.tell()
                terrain = Terrain(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f))


            
    print("TSFL: ", tsfl.signature, "Size: ", tsfl.size) 
    print("TRBF: ", trbf.signature)
    print("HDRX: ", hdrx.signature, "Size: ", hdrx.size, "Flag1: ", hdrx.flag1, "Flag2: ", hdrx.flag2, "Files: ", hdrx.fileCount)
    print("SECT: ", sect.signature, "Size: ", sect.size)
    f.close()