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
