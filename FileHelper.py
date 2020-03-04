import struct

def readString(f, count=0):
    if count is 0:
        c = ''
        output = ""
        while c is not 0:
            c = struct.unpack('B', f.read(1))[0]
            if c is 0:
                break
            output += chr(c)
    else:
        c = ''
        output = ""
        for x in range(count):
            c = struct.unpack('B', f.read(1))[0]
            output += chr(c)
    return output

def readUInt(f):
    return struct.unpack('I', f.read(4))[0]

def readUShort(f):
    return struct.unpack('H', f.read(2))[0]

def readFloat(f):
    return struct.unpack('f', f.read(4))[0]

# Not sure yet if that works
def readHFloat(f):
    return struct.unpack('f', f.read(2))[0]