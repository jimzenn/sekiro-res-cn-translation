"""
Compile translation/*.json  ->  build/msg/zhocn/{item,menu}.msgbnd.dcx  (+ build/font).

Uses sekiro-improved-chinese's binders as the base (correct FMG categories/names/hash),
replaces each FMG's content with the `cn` values from the JSON, repacks as DFLT DCX.

Usage:
  python3 compile_build.py            # write into ../build/
  python3 compile_build.py --check    # build in memory, verify, DO NOT write build/
"""
import os, json, sys, glob, shutil, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import fmglib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "sources")
TR   = os.path.join(ROOT, "translation")

BASE = {  # base binder = improved-chinese (vanilla CN, right structure)
  "item": f"{SRC}/improved-chinese/msg/zhocn/item.msgbnd.dcx",
  "menu": f"{SRC}/improved-chinese/msg/zhocn/menu.msgbnd.dcx",
}

def build_domain(domain):
    base_dcx = BASE[domain]
    bnd, _ = F.decompress_dcx(base_dcx)
    base_fmg_ids = {e['id'] for e in F.parse_bnd4(bnd)}
    new_blobs = {}
    warnings = []
    for jf in sorted(glob.glob(f"{TR}/{domain}/*.json")):
        d = json.load(open(jf, encoding="utf-8"))
        fid = d["fmg_id"]
        if fid not in base_fmg_ids:
            warnings.append(f"FMG {fid} ({d['fmg_name']}) not in base binder -> skipped")
            continue
        entries = {e["id"]: e["cn"] for e in d["entries"] if e["cn"] is not None}
        new_blobs[fid] = F.build_fmg(entries)
    newbnd = F.rebuild_bnd4(bnd, new_blobs)
    dcx = F.build_dcx_dflt(newbnd, base_dcx)
    return dcx, new_blobs, warnings

def verify(domain, dcx):
    """Decode the built dcx and confirm every FMG matches the JSON cn values."""
    rebnd, _ = F.decompress_dcx(dcx)
    tables = {e['id']: F.parse_fmg(e['blob']) for e in F.parse_bnd4(rebnd)}
    bad = 0
    for jf in glob.glob(f"{TR}/{domain}/*.json"):
        d = json.load(open(jf, encoding="utf-8"))
        if d["fmg_id"] not in tables: continue
        got = tables[d["fmg_id"]]
        for e in d["entries"]:
            if e["cn"] is not None and got.get(e["id"]) != e["cn"]:
                bad += 1
    return bad

def main():
    check = "--check" in sys.argv
    for domain in ("item", "menu"):
        dcx, blobs, warns = build_domain(domain)
        bad = verify(domain, dcx)
        for w in warns: print("  WARN:", w)
        print(f"  [{domain}] FMGs填充={len(blobs)} dcx={len(dcx)}B 校验不符={bad} {'OK' if bad==0 else 'FAIL'}")
        if not check:
            out = f"{ROOT}/build/msg/zhocn/{domain}.msgbnd.dcx"
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "wb").write(dcx)
    if not check:
        # copy fonts as-is
        fsrc = f"{SRC}/improved-chinese/font"
        fdst = f"{ROOT}/build/font"
        if os.path.isdir(fsrc):
            shutil.copytree(fsrc, fdst, dirs_exist_ok=True)
        print("  build/ written (msg/zhocn + font)")

if __name__ == "__main__":
    main()
