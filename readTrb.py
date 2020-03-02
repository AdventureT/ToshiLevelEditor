import struct
from . Labels import *
from . FileHelper import *


def read(filepath):
    f = open(filepath, "rb")
    tsfl = TSFL(readString(f,4), struct.unpack('i', f.read(4))[0])
    trbf = TRBF(readString(f,4))
    hdrx = HDRX(readString(f,4), struct.unpack('I', f.read(4))[0], struct.unpack('H', f.read(2))[0], struct.unpack('H', f.read(2))[0], struct.unpack('I', f.read(4))[0])
    for x in range(hdrx.fileCount):
        hdrx.files.append(HDRX.File(struct.unpack('H', f.read(2))[0], struct.unpack('H', f.read(2))[0], struct.unpack('I', f.read(4))[0], struct.unpack('I', f.read(4))[0], struct.unpack('I', f.read(4))[0]))
    sect = SECT(readString(f,4), struct.unpack('I', f.read(4))[0])
    chunk = f.tell()
    f.seek(sect.size,1)
    relc = RELC(readString(f,4), struct.unpack('I', f.read(4))[0])
    f.seek(relc.size,1)
    symb = SYMB(readString(f,4), struct.unpack('I', f.read(4))[0], struct.unpack('I', f.read(4))[0])
    cur = f.tell()
    for x in range(symb.symbolCount):
        c = SYMB.Symbol("", struct.unpack('H', f.read(2))[0], struct.unpack('I', f.read(4))[0], struct.unpack('H', f.read(2))[0], struct.unpack('I', f.read(4))[0])
        cu = f.tell()
        f.seek(cur + (symb.symbolCount * 12) + c.nameOffset,0)
        c.name = readString(f)
        f.seek(cu,0)
        symb.symbols.append(c)
        #print("SYMB ",x,": ", c.name)
    f.seek(chunk,0)
    baseChunk = chunk
    for x in range(len(symb.symbols)):
        if symb.symbols[x].Id is not 0:
            chunk = hdrx.files[symb.symbols[x].Id - 1].fileSize + baseChunk
        f.seek(chunk + symb.symbols[x].dataOffset, 0)
        if symb.symbols[x].name == "tmod":
            lsss = f.tell()
            tmod = TMOD(TMOD.Header(struct.unpack('I', f.read(4))[0], struct.unpack('I', f.read(4))[0], struct.unpack('I', f.read(4))[0],struct.unpack('I', f.read(4))[0],struct.unpack('I', f.read(4))[0]
            ,struct.unpack('I', f.read(4))[0],struct.unpack('I', f.read(4))[0], struct.unpack('I', f.read(4))[0]))
    print("TSFL: ", tsfl.signature, "Size: ", tsfl.size) 
    print("TRBF: ", trbf.signature)
    print("HDRX: ", hdrx.signature, "Size: ", hdrx.size, "Flag1: ", hdrx.flag1, "Flag2: ", hdrx.flag2, "Files: ", hdrx.fileCount)
    print("SECT: ", sect.signature, "Size: ", sect.size)