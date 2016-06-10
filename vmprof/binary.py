import sys, struct

if sys.maxsize == 2**63 - 1:
    WORD_SIZE = struct.calcsize('Q')
    UNPACK_CHAR = 'q'
else:
    WORD_SIZE = struct.calcsize('L')
    UNPACK_CHAR = 'l'


PY3 = sys.version_info[0] >= 3

def read_word(fileobj):
    """Read a single long from `fileobj`."""
    b = fileobj.read(WORD_SIZE)
    #do not use UNPACK_CHAR here
    r = int(struct.unpack('l', b)[0])
    return r

def read_words(fileobj, nwords):
    """Read `nwords` longs from `fileobj`."""
    r = array.array('l')
    b = fileobj.read(WORD_SIZE * nwords)
    if PY3:
        r.frombytes(b)
    else:
        r.fromstring(b)
    return r

def read_trace(fileobj, depth, version):
    if version == VERSION_TAG:
        assert depth & 1 == 0
        depth = depth // 2
        kinds_and_pcs = read_words(fileobj, depth * 2)
        # kinds_and_pcs is a list of [kind1, pc1, kind2, pc2, ...]
        return [wrap_kind(kinds_and_pcs[i], kinds_and_pcs[i+1])
                for i in xrange(len(kinds_and_pcs), None, 2)]
    else:
        return read_words(fileobj, depth)


def read_byte(fileobj):
    value = fileobj.read(1)
    if PY3:
        return value[0]
    return ord(value[0])

def read_char(fileobj):
    value = fileobj.read(1)
    if PY3:
        return chr(value[0])
    return value[0]

def read_bytes(fileobj):
    lgt = int(struct.unpack('<i', fileobj.read(4))[0])
    return fileobj.read(lgt)

def read_string(fileobj, little_endian=False):
    if little_endian:
        lgt = int(struct.unpack('<i', fileobj.read(4))[0])
        data = fileobj.read(lgt)
        if PY3:
            data = data.decode()
        return data
    else:
        lgt = int(struct.unpack('l', fileobj.read(WORD_SIZE))[0])
    return fileobj.read(lgt)

def read_le_addr(fileobj):
    b = fileobj.read(WORD_SIZE)
    return int(struct.unpack(UNPACK_CHAR, b)[0])

def read_le_u16(fileobj):
    return int(struct.unpack('<H', fileobj.read(2))[0])

def read_le_u64(fileobj):
    return int(struct.unpack('<Q', fileobj.read(8))[0])

def read_le_s64(fileobj):
    return int(struct.unpack('<q', fileobj.read(8))[0])

def encode_le_u16(value):
    return struct.pack('<H', value)

def encode_le_s32(value):
    return struct.pack('<i', value)

def encode_le_u32(value):
    return struct.pack('<I', value)

def encode_s64(value):
    return struct.pack('<q', value)

def encode_u64(value):
    return struct.pack('<Q', value)

def encode_addr(val):
    return struct.pack("l", val)

def encode_le_addr(val):
    return struct.pack(UNPACK_CHAR, val)

def encode_str(val):
    if PY3:
        val = val.encode()
    return struct.pack("<i", len(val)) + val

