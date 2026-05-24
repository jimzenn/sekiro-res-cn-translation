"""
Sekiro msgbnd (.msgbnd.dcx) decode/encode library — pure Python, no Windows/Oodle deps.

Pipeline:  .dcx  <-DFLT(zlib)->  BND4 binder  <->  FMG text files  <->  {id: text}

Only DFLT-compressed DCX is supported (vanilla Sekiro Oodle/KRAK is NOT handled here;
we don't need it — see MEMORY.md). All files we build are DFLT, which the game reads fine.
"""
import struct, zlib

# ---------------- DCX ----------------
def decompress_dcx(src):
    data = open(src, 'rb').read() if isinstance(src, str) else src
    assert data[:4] == b'DCX\x00', "not a DCX"
    method = data[0x28:0x2c]
    comp   = struct.unpack_from('>I', data, 0x20)[0]
    dca    = data.find(b'DCA\x00')
    start  = dca + 8
    if method == b'DFLT':
        return zlib.decompress(data[start:start+comp]), method
    return None, method  # KRAK/Oodle not supported

def build_dcx_dflt(bnd_bytes, template_path):
    """Wrap BND4 bytes in a DFLT DCX, reusing the header template from an existing DFLT .dcx."""
    tmpl = open(template_path, 'rb').read()
    assert tmpl[0x28:0x2c] == b'DFLT', "template is not DFLT"
    dca = tmpl.find(b'DCA\x00')
    header = bytearray(tmpl[:dca + 8])
    z = zlib.compress(bnd_bytes, 9)
    struct.pack_into('>I', header, 0x1c, len(bnd_bytes))  # uncompressed size
    struct.pack_into('>I', header, 0x20, len(z))          # compressed size
    return bytes(header) + z

# ---------------- BND4 ----------------
def parse_bnd4(data):
    assert data[:4] == b'BND4'
    fileCount      = struct.unpack_from('<i', data, 0x0c)[0]
    fileHeaderSize = struct.unpack_from('<q', data, 0x20)[0]
    ents, off = [], 0x40
    for _ in range(fileCount):
        comp    = struct.unpack_from('<q', data, off+8)[0]
        uncomp  = struct.unpack_from('<q', data, off+16)[0]
        dataOff = struct.unpack_from('<I', data, off+24)[0]
        eid     = struct.unpack_from('<i', data, off+28)[0]
        nameOff = struct.unpack_from('<i', data, off+32)[0]
        nm, p = b'', nameOff
        while data[p:p+2] != b'\x00\x00':
            nm += data[p:p+2]; p += 2
        ents.append(dict(id=eid, name=nm.decode('utf-16le'), dataOffset=dataOff,
                         uncomp=uncomp, blob=data[dataOff:dataOff+uncomp], hdr_off=off))
        off += fileHeaderSize
    return ents

def rebuild_bnd4(orig, new_blobs, align=0x10):
    """Surgical rebuild: keep header/entry-table/names/hash-table prefix, repatch each entry's
       size+offset, and reassemble the data region. new_blobs: {entry_id: fmg_bytes}."""
    ents = parse_bnd4(orig)
    data_start = min(e['dataOffset'] for e in ents)
    prefix = bytearray(orig[:data_start])
    order = sorted(ents, key=lambda e: e['dataOffset'])
    data = bytearray()
    cur = data_start
    new_off = {}
    for e in order:
        pad = (-cur) % align
        data += b'\x00' * pad; cur += pad
        blob = new_blobs.get(e['id'], e['blob'])
        new_off[e['id']] = cur
        data += blob; cur += len(blob)
    for e in ents:
        blob = new_blobs.get(e['id'], e['blob']); sz = len(blob)
        struct.pack_into('<q', prefix, e['hdr_off']+8,  sz)
        struct.pack_into('<q', prefix, e['hdr_off']+16, sz)
        struct.pack_into('<I', prefix, e['hdr_off']+24, new_off[e['id']])
    return bytes(prefix) + bytes(data)

# ---------------- FMG ----------------
def parse_fmg(blob):
    assert blob[0] == 0
    wide = blob[2] == 2
    groupCount  = struct.unpack_from('<i', blob, 0x0c)[0]
    stringCount = struct.unpack_from('<i', blob, 0x10)[0]
    if wide:
        soo = struct.unpack_from('<q', blob, 0x18)[0]; gstart, gstride = 0x28, 16
    else:
        soo = struct.unpack_from('<i', blob, 0x14)[0]; gstart, gstride = 0x1c, 12
    groups, p = [], gstart
    for _ in range(groupCount):
        oi, fi, li = struct.unpack_from('<iii', blob, p); groups.append((oi, fi, li)); p += gstride
    offs, op = [], soo
    for _ in range(stringCount):
        if wide: o = struct.unpack_from('<q', blob, op)[0]; op += 8
        else:    o = struct.unpack_from('<i', blob, op)[0]; op += 4
        offs.append(o)
    res = {}
    for oi, fi, li in groups:
        for k, sid in enumerate(range(fi, li+1)):
            o = offs[oi+k]
            if o == 0: res[sid] = None; continue
            s, q = b'', o
            while blob[q:q+2] != b'\x00\x00': s += blob[q:q+2]; q += 2
            res[sid] = s.decode('utf-16le')
    return res

def build_fmg(entries):
    """entries: {id: text or None}. Returns Sekiro wide (v2) FMG bytes."""
    ids = sorted(entries)
    stringCount = len(ids)
    groups, i = [], 0
    while i < len(ids):
        j = i
        while j+1 < len(ids) and ids[j+1] == ids[j] + 1: j += 1
        groups.append((i, ids[i], ids[j])); i = j + 1
    groupCount = len(groups)
    soo = 0x28 + groupCount * 16
    string_data_start = soo + stringCount * 8
    sblob = bytearray(); seen = {}; offsets = []
    for sid in ids:
        t = entries[sid]
        if t is None: offsets.append(0); continue
        if t in seen: offsets.append(seen[t]); continue
        o = string_data_start + len(sblob); seen[t] = o
        sblob += t.encode('utf-16le') + b'\x00\x00'; offsets.append(o)
    fileSize = string_data_start + len(sblob)
    out = bytearray(string_data_start)
    out[2] = 2
    struct.pack_into('<i', out, 0x04, fileSize)
    struct.pack_into('<i', out, 0x08, 1)
    struct.pack_into('<i', out, 0x0c, groupCount)
    struct.pack_into('<i', out, 0x10, stringCount)
    struct.pack_into('<i', out, 0x14, 0xFF)
    struct.pack_into('<q', out, 0x18, soo)
    p = 0x28
    for oi, fi, li in groups:
        struct.pack_into('<iii', out, p, oi, fi, li); p += 16
    p = soo
    for o in offsets:
        struct.pack_into('<q', out, p, o); p += 8
    return bytes(out) + bytes(sblob)

# ---------------- high level ----------------
def load_msgbnd(path):
    """Return {fmg_id: (fmg_name, {string_id: text|None})} for a DFLT .dcx."""
    bnd, method = decompress_dcx(path)
    if bnd is None: raise RuntimeError(f"{path}: {method} not supported")
    out = {}
    for e in parse_bnd4(bnd):
        out[e['id']] = (e['name'].split('\\')[-1], parse_fmg(e['blob']))
    return out
