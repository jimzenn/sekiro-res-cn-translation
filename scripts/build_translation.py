"""
Generate aligned translation/*.json from the source .dcx files.

For each FMG category (per domain item/menu), align every string id across:
  cn_improved      = sekiro-improved-chinese  (better vanilla CN; STYLE BASE)
  cn_resurrection  = Resurrection's existing zhocn (item only; menu is Oodle/unread)
  jp / en          = Resurrection's Japanese / English (source for new mod content)

Working value `cn` + `status` are derived:
  from_improved      -> improved-chinese has it (use as-is, the good vanilla base)
  needs_polish       -> only Resurrection CN has it (mod content already translated; polish to style)
  needs_translation  -> no CN anywhere (new mod content; cn falls back to en/jp, TO TRANSLATE)
"""
import os, json, sys
sys.path.insert(0, os.path.dirname(__file__))
import fmglib as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "sources")
OUT  = os.path.join(ROOT, "translation")

SOURCES = {
  "item": {
    "cn_improved":     f"{SRC}/improved-chinese/msg/zhocn/item.msgbnd.dcx",
    "cn_resurrection": f"{SRC}/resurrection/msg/zhocn/item.msgbnd.dcx",
    "jp":              f"{SRC}/resurrection/msg/jpnjp/item.msgbnd.dcx",
    "en":              f"{SRC}/resurrection/msg/engus/item.msgbnd.dcx",
  },
  "menu": {
    "cn_improved":     f"{SRC}/improved-chinese/msg/zhocn/menu.msgbnd.dcx",
    # resurrection zhocn/menu is Oodle/KRAK -> unread -> intentionally absent
    "jp":              f"{SRC}/resurrection/msg/jpnjp/menu.msgbnd.dcx",
    "en":              f"{SRC}/resurrection/msg/engus/menu.msgbnd.dcx",
  },
}

def main():
    summary = {}
    for domain, paths in SOURCES.items():
        loaded = {k: F.load_msgbnd(p) for k, p in paths.items()}
        # reference category set = union of all sources' FMG ids
        fmg_ids = set()
        for d in loaded.values(): fmg_ids |= set(d.keys())
        os.makedirs(f"{OUT}/{domain}", exist_ok=True)
        dom_counts = {"from_improved":0,"needs_polish":0,"needs_translation":0}
        for fid in sorted(fmg_ids):
            name = None
            cats = {}
            for k, d in loaded.items():
                if fid in d:
                    nm, table = d[fid]; name = name or nm; cats[k] = table
                else:
                    cats[k] = {}
            imp, res = cats.get("cn_improved",{}), cats.get("cn_resurrection",{})
            jp, en   = cats.get("jp",{}), cats.get("en",{})
            ids = set()
            for t in (imp,res,jp,en):
                ids |= {i for i,v in t.items() if v is not None}
            if not ids: continue
            entries = []
            for sid in sorted(ids):
                e_imp, e_res = imp.get(sid), res.get(sid)
                e_jp, e_en   = jp.get(sid), en.get(sid)
                if e_imp is not None:
                    cn, st = e_imp, "from_improved"
                elif e_res is not None:
                    cn, st = e_res, "needs_polish"
                else:
                    cn, st = (e_en if e_en is not None else e_jp), "needs_translation"
                dom_counts[st]+=1
                entries.append({"id":sid,"status":st,"cn":cn,
                                "en":e_en,"jp":e_jp,
                                "cn_improved":e_imp,"cn_resurrection":e_res})
            safe = name.replace(".fmg","") if name else str(fid)
            fn = f"{OUT}/{domain}/{fid:03d}_{safe}.json"
            with open(fn,"w",encoding="utf-8") as f:
                json.dump({"fmg_id":fid,"fmg_name":safe,"domain":domain,
                           "count":len(entries),"entries":entries},
                          f, ensure_ascii=False, indent=2)
        summary[domain]=dom_counts
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__=="__main__":
    main()
