from io import BufferedReader
import struct
import bpy
from mathutils import Vector
from . Labels import *
from . FileHelper import *
from . ModelData import *
import os

md = []
td = []
#filepath = str
# trb = TRB
#f = BufferedReader


def readTrbSections(f: BufferedReader):
    tsfl = TSFL(readString(f, 4), readUInt(f))
    trbf = TRBF(readString(f, 4))
    hdrx = HDRX(readString(f, 4), readUInt(
        f), readUShort(f), readUShort(f), readUInt(f))
    for x in range(hdrx.fileCount):
        file = HDRX.File(readUShort(f), readUShort(
            f), readUInt(f), readUInt(f), readUInt(f))
        if (x != 0):
            file.fileSize += hdrx.files[x-1].fileSize
        hdrx.files.append(file)
    sect = SECT(readString(f, 4), readUInt(f))
    chunk = f.tell()
    f.seek(sect.size, 1)
    relc = RELC(readString(f, 4), readUInt(f))
    f.seek(relc.size, 1)
    symb = SYMB(readString(f, 4), readUInt(f), readUInt(f))
    cur = f.tell()
    for x in range(symb.symbolCount):
        c = SYMB.Symbol("", readUShort(f), readUInt(f),
                        readUShort(f), readUInt(f))
        cu = f.tell()
        f.seek(cur + (symb.symbolCount * 12) + c.nameOffset, 0)
        c.name = readString(f)
        f.seek(cu, 0)
        symb.symbols.append(c)
        print("SYMB ", x, ": ", c.name)
    trb = TRB(tsfl, trbf, hdrx, sect, relc, symb)
    trb.chunk = chunk
    return trb


def readModel(mdIndex, f: BufferedReader, chunk : int):
    meshNames = []
    tmod = TMOD(TMOD.Header(readUInt(f), readUInt(f), readFloat(
        f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)))
    f.seek(tmod.header.modelFileNameOffset + chunk, 0)
    modelName = readString(f)
    f.seek(tmod.header.meshInfoOffset + chunk, 0)
    tmod.meshesInfo = TMOD.MeshesInfo(readUInt(f), readUInt(f), readUInt(f))
    for y in range(tmod.meshesInfo.meshCount):
        tmod.meshesInfo.meshInfoOffsets.append(readUInt(f))
    print("Mesh Count: ", tmod.meshesInfo.meshCount, "Model Name: ", modelName)
    for z in range(tmod.meshesInfo.meshCount):
        f.seek(tmod.meshesInfo.meshInfoOffsets[z] + chunk, 0)
        tmod.meshInfos.append(TMOD.MeshInfo(readUInt(f), readUInt(
            f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)))
        f.seek(tmod.meshInfos[z].meshNameOffset + chunk, 0)
        meshName = readString(f)
        meshNames.append(meshName)
        print("\t Mesh Name: ", meshName)
    for j in range(tmod.meshesInfo.meshCount):
        f.seek(tmod.meshInfos[j].meshSubInfoOffset + chunk, 0)
        tmod.meshSubInfos.append(TMOD.MeshSubInfo(readUInt(f), readUInt(
            f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)))
        tmod.meshSubInfos[j].faceCount /= 3
        print("Vertices: ", tmod.meshSubInfos[j].vertexCount,
              " Faces: ", tmod.meshSubInfos[j].faceCount)
    md.append(ModelData(modelName, meshNames))
    for i in range(tmod.meshesInfo.meshCount):
        verts = []
        normals = []
        uvs = []
        faces = []
        f.seek(tmod.meshSubInfos[i].vertexOffset + chunk, 0)
        for l in range(tmod.meshSubInfos[i].vertexCount):
            verts.append(Vector((readFloat(f), readFloat(f), readFloat(f))))
            normals.append(Vector((readFloat(f), readFloat(f), readFloat(f))))
            f.seek(8, 1)
            uvs.append(Vector((readFloat(f), -readFloat(f))))
            f.seek(4, 1)
        f.seek(tmod.meshSubInfos[i].faceOffset + chunk, 0)
        for p in range(int(tmod.meshSubInfos[i].faceCount)):
            faces.append([readUShort(f), readUShort(f), readUShort(f)])
        md[mdIndex].meshData.append(
            ModelData.MeshData(verts, faces, normals, uvs))
    mdIndex += 1
    del tmod
    return mdIndex

# Basically reading Entity models
def readWorld(mdIndex: int, f: BufferedReader, chunk : int):
    meshNames = []
    twld = TWLD(TWLD.Header(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f),
                            {readFloat(f), readFloat(f), readFloat(f), readFloat(f)}))
    f.seek(twld.header.modelFileNameOffset + chunk, 0)
    modelName = readString(f)
    f.seek(twld.header.meshInfoOffset + chunk, 0)
    # Very unclean; there might be more 'UnknownInfos' than one
    twld.unknownInfos.append(TWLD.UnknownInfo(
        readUInt(f), readUInt(f), readUInt(f)))
    f.seek(twld.unknownInfos[0].unknownInfo2Offset + chunk, 0)
    twld.unknownInfos2.append(TWLD.UnknownInfo2(
        readUInt(f), readUInt(f), readUInt(f)))
    f.seek(twld.unknownInfos2[0].unknownInfo3Offset + chunk, 0)
    twld.unknownInfos3.append(TWLD.UnknownInfo3(readUInt(f), {readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f),
                                                              readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(
                                                                  f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f),
                                                              readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(
                                                                  f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f),
                                                              readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f)}))
    twld.meshesInfo = TWLD.MeshesInfo(readUInt(f), readUInt(f), readUInt(f))
    for g in range(twld.meshesInfo.meshInfoOffsetsCount):
        f.seek(twld.meshesInfo.meshInfoOffsetsOffset + chunk, 0)
        twld.meshesInfo.meshInfoOffsets.append(readUInt(f))
    tell = f.tell()
    for h in range(twld.meshesInfo.meshInfoOffsetsCount):
        f.seek(twld.meshesInfo.meshInfoOffsets[h] + chunk, 0)
        twld.meshInfos.append(TWLD.MeshInfo(
            {readFloat(f), readFloat(f), readFloat(f), readFloat(f)}, readUInt(f)))
    for c in range(twld.meshesInfo.meshInfoOffsetsCount):
        f.seek(twld.meshInfos[c].meshSubInfoOffset + chunk, 0)
        twld.meshSubInfos.append(TWLD.MeshSubInfo(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f),
                                                  readUInt(f), readUInt(f), readUInt(f)))
        f.seek(twld.meshSubInfos[c].meshNameOffset + chunk, 0)
        meshNames.append(readString(f))
        twld.meshSubInfos[c].faceCount /= 3
    md.append(ModelData(modelName, meshNames))
    for v in range(twld.meshesInfo.meshInfoOffsetsCount):
        verts = []
        normals = []
        uvs = []
        faces = []
        f.seek(twld.meshSubInfos[v].vertexOffset + chunk, 0)
        for w in range(twld.meshSubInfos[v].vertexCount):
            verts.append(Vector((readFloat(f), readFloat(f), readFloat(f))))
            normals.append(Vector((readFloat(f), readFloat(f), readFloat(f))))
            f.seek(12, 1)
            uvs.append(Vector((readFloat(f), -readFloat(f))))
            f.seek(8, 1)
        f.seek(twld.meshSubInfos[v].faceOffset + chunk, 0)
        for q in range(int(twld.meshSubInfos[v].faceCount)):
            faces.append([readUShort(f), readUShort(f), readUShort(f)])
        md[mdIndex].meshData.append(
            ModelData.MeshData(verts, faces, normals, uvs))
    mdIndex += 1
    del twld
    return mdIndex

def readTerrain(filepath : str):
    f = open(filepath + "\\terrain.trb", "rb")
    trb = readTrbSections(f)
    chunk = trb.chunk
    for x in range(len(trb.symb.symbols)):
        if trb.symb.symbols[x].Id is not 0:
            chunk = trb.hdrx.files[trb.symb.symbols[x].Id -
                                   1].fileSize + trb.chunk
        f.seek(chunk + trb.symb.symbols[x].dataOffset, 0)
        if trb.symb.symbols[x].name == "Terrain_Main":
            break
    tell = f.tell()
    terrain = Terrain(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f),
                      readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f))
    f.seek(terrain.unknownInfoOffset + trb.chunk, 0)
    for k in range(terrain.unknownInfoCount):
        unknownInfo = Terrain.UnknownInfo(readUInt(f), readUInt(f), readUInt(f), readUInt(f), readUInt(f), {readUInt(f), readUInt(f), readUInt(f)}, readUInt(f),
                                          {readUInt(f), readUInt(f), readUInt(f)}, readUInt(f), {readUInt(f), readUInt(f), readUInt(f)})
        re = f.tell()
        f.seek(unknownInfo.coordsInfoOffset + trb.chunk, 0)
        coordsInfo = Terrain.UnknownInfo.CoordsInfo(readUInt(f), readUInt(f))
        f.seek(coordsInfo.coordsOffset + trb.chunk, 0)
        pos = Vector((readFloat(f), readFloat(f), readFloat(f)))
        if (unknownInfo.modelNameOffset is not 0):
            f.seek(unknownInfo.modelNameOffset + trb.chunk, 0)
            td.append(TerrainData(readString(f), pos))
        else:
            f.seek(unknownInfo.typeNameOffset + trb.chunk, 0)
            td.append(TerrainData(readString(f), pos))
        f.seek(re, 0)
        #print(td[k].modelName)
    # Gets The directory
    #dire = os.path.dirname(filepath)
    # Loading RegionAssets at the moment
    # Read RegionRuntimeData for all necessary models and level data
    #dire += "\\RegionAssets.trb"


def readRegionRuntimeData(filepath : str):
    # Load RegionRuntimeData
    f = open(filepath + "\\RegionRuntimeData.trb", "rb")
    trb = readTrbSections(f)
    f.seek(trb.chunk, 0)
    offset = readUInt(f)
    count = readUInt(f)
    f.seek(trb.chunk + offset, 0)
    offsetToRegionName = readUInt(f)
    #tell = f.tell()
    #f.seek(trb.chunk + offsetToRegionName, 0)
    #regionName = readString(f)
    #f.seek(tell, 0)
    countLevelAssets = readUInt(f)
    offsetToLevelAssets = readUInt(f)
    countSFX = readUInt(f)
    offsetToSFX = readUInt(f)
    countTGAStruct = readUInt(f)
    offsetTGAStruct = readUInt(f)

    f.seek(trb.chunk + offsetToRegionName, 0)
    regionName = readString(f)
    f.seek(trb.chunk + offsetToLevelAssets, 0)
    levelAssets = []
    for i in range(countLevelAssets):
        f.seek(trb.chunk + offsetToLevelAssets + i * 4, 0)
        off = readUInt(f)
        f.seek(trb.chunk + off, 0)
        levelAssets.append(readString(f))
    return levelAssets


def readAssets(assetNames: list, filepath : str):
    for i in range(len(assetNames)):
        f = open(filepath + "\\" +assetNames[i] + ".trb", "rb")
        trb = readTrbSections(f)
        mdIndex = 0
        chunk = trb.chunk
        for x in range(len(trb.symb.symbols)):
            if trb.symb.symbols[x].Id is not 0:
                chunk = trb.hdrx.files[trb.symb.symbols[x].Id -
                                       1].fileSize + trb.chunk
            f.seek(chunk + trb.symb.symbols[x].dataOffset, 0)
            if trb.symb.symbols[x].name == "tmod":
                mdIndex = readModel(mdIndex, f, chunk)
            #if trb.symb.symbols[x].name == "twld":
                #mdIndex = readWorld(mdIndex, f, chunk)
            # TODO: TTEX, TMTL, TTL, TSKL?


def read(filename : str, t):
    filepath = os.path.dirname(filename)
    levelAssets = readRegionRuntimeData(filepath)
    readAssets(levelAssets, filepath)
    readTerrain(filepath)
    exportData()
    #f = open(filepath, "rb")
    #trb = readTrbSections()
    # f.seek(trb.chunk,0)
    #baseChunk = trb.chunk
    #mdIndex = 0
    #x2 = 0
    # for x in range(len(trb.symb.symbols)):
    #    if trb.symb.symbols[x].Id is not 0:
    #        chunk = trb.hdrx.files[trb.symb.symbols[x].Id - 1].fileSize + baseChunk
    #    f.seek(chunk + trb.symb.symbols[x].dataOffset, 0)
    #    if t is 0:
    #        if trb.symb.symbols[x].name == "tmod":
    #            readModel(mdIndex, x2)
    #        if trb.symb.symbols[x].name == "twld":
    #            readWorld(mdIndex)
    #    else:
    #        if trb.symb.symbols[x].name == "Terrain_Main":
    #            readTerrain()
    #            # Why recursion?
    #            # read(dire, 0)
    # if t is 0:
    #    print("TSFL: ", trb.tsfl.signature, "Size: ", trb.tsfl.size)
    #    print("TRBF: ", trb.trbf.signature)
    #    print("HDRX: ", trb.hdrx.signature, "Size: ", trb.hdrx.size, "Flag1: ", trb.hdrx.flag1, "Flag2: ", trb.hdrx.flag2, "Files: ", trb.hdrx.fileCount)
    #    print("SECT: ", trb.sect.signature, "Size: ", trb.sect.size)
    #    f.close()
    #    exportData()
    #    print("Finished")


def exportData():
    for i in range(len(md)):
        tdpos = -1
        mdlName = os.path.splitext(md[i].modelName)[0]
        for j in range(len(td)):
            if (td[j].modelName == mdlName):
                tdpos = j
                break
        if (tdpos != -1):
            parent_object = bpy.data.objects.new(md[i].modelName, None)
            parent_object.location = (td[tdpos].position)
            bpy.context.scene.collection.objects.link(parent_object)

            for y in range(len(md[i].meshNames)):
                mesh = bpy.data.meshes.new(md[i].meshNames[y])
                obj = bpy.data.objects.new(md[i].meshNames[y], mesh)
                obj.data.from_pydata(
                    md[i].meshData[y].vertices, [], md[i].meshData[y].faces)
                for face in mesh.polygons:
                    face.use_smooth = True  # loop normals have effect only if smooth shading
                obj.data.normals_split_custom_set_from_vertices(
                    md[i].meshData[y].normals)
                obj.parent = parent_object
                bpy.context.scene.collection.objects.link(obj)
        else:
            print("Could not find a model called",
                  md[i].modelName, "in terrain.trb")
