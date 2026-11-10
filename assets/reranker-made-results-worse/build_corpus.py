"""Turn the MITRE ATT&CK STIX bundles (attack-stix-data) into one Markdown file per object.

Condense's agent ingests .md/.txt/.pdf/... but not .json, so the raw bundles are rendered into a
Markdown corpus: tactics, techniques, mitigations, groups, software and campaigns from the latest
Enterprise, Mobile and ICS bundles. Revoked and deprecated objects are left out. Relationships
("uses", "mitigates", "attributed-to", "subtechnique-of", "detects") are resolved to names and
carry MITRE's own procedure text.

    python3 -I build_corpus.py attack-stix-data corpus
"""

import json
import os
import re
import shutil
import sys
from collections import defaultdict

DOMAINS = {
    "enterprise-attack": ("Enterprise", "mitre-attack"),
    "mobile-attack": ("Mobile", "mitre-mobile-attack"),
    "ics-attack": ("ICS", "mitre-ics-attack"),
}
KIND = {
    "x-mitre-tactic": "tactics",
    "attack-pattern": "techniques",
    "course-of-action": "mitigations",
    "intrusion-set": "groups",
    "malware": "software",
    "tool": "software",
    "campaign": "campaigns",
    "x-mitre-detection-strategy": "detection",
}
LABEL = {"tactics": "tactic", "techniques": "technique", "mitigations": "mitigation", "groups": "group",
         "software": "software", "campaigns": "campaign"}
CITE = re.compile(r"\s*\(Citation:[^)]*\)")
MDLINK = re.compile(r"\[([^\]]+)\]\((?:https?://)[^)]*\)")
CODE = re.compile(r"</?code>")


def clean(s):
    s = CITE.sub("", s or "")
    s = MDLINK.sub(r"\1", s)
    s = CODE.sub("`", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def oneline(s):
    return re.sub(r"\s*\n+\s*", " ", s or "").strip()


def ext_id(o):
    for r in o.get("external_references", []):
        if r.get("source_name") in ("mitre-attack", "mitre-mobile-attack", "mitre-ics-attack") and r.get("external_id"):
            return r["external_id"], r.get("url")
    return None, None


def slug(s, n=80):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].rstrip("-")


def load(src):
    """Latest bundle of each domain, merged by STIX id (objects shared across domains appear once)."""
    objs, rels, version = {}, {}, {}
    for d, (dname, _) in DOMAINS.items():
        path = os.path.join(src, d, d + ".json")
        bundle = json.load(open(path, encoding="utf-8"))["objects"]
        for o in bundle:
            if o.get("revoked") or o.get("x_mitre_deprecated"):
                continue
            if o["type"] == "relationship":
                rels[o["id"]] = o
            elif o["type"] == "x-mitre-collection":
                version[dname] = o.get("x_mitre_version")
            elif o["type"] == "x-mitre-analytic":
                analytics[o["id"]] = o
            elif o["type"] in KIND:
                prev = objs.get(o["id"])
                o = dict(o)
                o["_domains"] = sorted(set((prev or {}).get("_domains", [])) | {dname})
                objs[o["id"]] = o
    return objs, list(rels.values()), version


def analytic_lines(strategy):
    lines = []
    for ref_id in strategy.get("x_mitre_analytic_refs", []):
        a = analytics.get(ref_id)
        if not a:
            continue
        aid, _ = ext_id(a)
        plats = ", ".join(a.get("x_mitre_platforms", []))
        line = "  - %s%s: %s" % (aid or a["name"], " (%s)" % plats if plats else "", oneline(clean(a.get("description"))))
        logs = ["%s %s" % (l.get("name", ""), "(%s)" % l["channel"] if l.get("channel") else "")
                for l in a.get("x_mitre_log_source_references", [])]
        if logs:
            line += " Log sources: " + "; ".join(x.strip() for x in logs) + "."
        lines.append(line)
    return lines


def build(src, out):
    objs, rels, version = load(src)
    ids = {}
    for sid, o in objs.items():
        aid, url = ext_id(o)
        if aid:
            o["_aid"], o["_url"] = aid, url
            ids[sid] = o

    parent = {}
    subs = defaultdict(list)
    out_links = defaultdict(list)  # source sid -> [(rel_type, target sid, text)]
    in_links = defaultdict(list)   # target sid -> [(rel_type, source sid, text)]
    for r in rels:
        s, t, kind = r["source_ref"], r["target_ref"], r["relationship_type"]
        if s not in ids or t not in ids:
            continue
        if kind == "subtechnique-of":
            parent[s] = t
            subs[t].append(s)
            continue
        text = oneline(clean(r.get("description")))
        out_links[s].append((kind, t, text))
        in_links[t].append((kind, s, text))

    def title(sid):
        o = ids[sid]
        if sid in parent:
            return "%s: %s" % (ids[parent[sid]]["name"], o["name"])
        return o["name"]

    def ref(sid):
        return "%s %s" % (ids[sid]["_aid"], title(sid))

    def kind_of(sid):
        return KIND[ids[sid]["type"]]

    def bullets(items, with_kind=False):
        lines = []
        for _, sid, text in sorted(items, key=lambda x: ids[x[1]]["_aid"]):
            head = "**%s**" % ref(sid)
            if with_kind:
                head += " (%s)" % LABEL.get(kind_of(sid), kind_of(sid))
            lines.append("- %s — %s" % (head, text) if text else "- %s" % head)
        return lines

    tactic_by_short = {}
    for sid, o in ids.items():
        if o["type"] == "x-mitre-tactic":
            for d in o["_domains"]:
                tactic_by_short[(DOMAINS_BY_NAME[d], o["x_mitre_shortname"])] = sid
    techniques_by_tactic = defaultdict(list)
    for sid, o in ids.items():
        if o["type"] == "attack-pattern":
            for p in o.get("kill_chain_phases", []):
                tac = tactic_by_short.get((p["kill_chain_name"], p["phase_name"]))
                if tac:
                    techniques_by_tactic[tac].append(sid)

    if os.path.isdir(out):
        shutil.rmtree(out)
    counts = defaultdict(int)
    for sid, o in sorted(ids.items(), key=lambda x: x[1]["_aid"]):
        kind = KIND[o["type"]]
        if kind == "detection":
            continue  # rendered inside the technique it detects
        md = ["# %s — %s" % (o["_aid"], title(sid)), ""]
        meta = [("Type", LABEL[kind] + (" (%s)" % o["type"] if kind == "software" else "")),
                ("Domain", ", ".join(d + " ATT&CK" for d in o["_domains"]))]
        if kind == "techniques":
            if sid in parent:
                meta[0] = ("Type", "sub-technique of %s" % ref(parent[sid]))
            tacs = sorted({ids[t]["name"] for t in [tactic_by_short.get((p["kill_chain_name"], p["phase_name"]))
                                                     for p in o.get("kill_chain_phases", [])] if t})
            meta.append(("Tactics", ", ".join(tacs)))
        aliases = [a for a in o.get("aliases", o.get("x_mitre_aliases", [])) if a != o["name"]]
        if aliases:
            meta.append(("Also known as", ", ".join(aliases)))
        if o.get("x_mitre_platforms"):
            meta.append(("Platforms", ", ".join(o["x_mitre_platforms"])))
        if kind == "campaigns":
            meta.append(("First seen", (o.get("first_seen") or "?")[:10]))
            meta.append(("Last seen", (o.get("last_seen") or "?")[:10]))
        meta.append(("ATT&CK URL", o["_url"]))
        meta.append(("Last modified", o.get("modified", "")[:10]))
        md += ["- **%s:** %s" % kv for kv in meta] + ["", "## Description", "", clean(o.get("description")) or "_None._"]

        outs, ins = out_links[sid], in_links[sid]
        sections = []
        if kind == "tactics":
            sections.append(("Techniques", ["- **%s**" % ref(t) for t in
                                            sorted(techniques_by_tactic[sid], key=lambda t: ids[t]["_aid"])]))
        if kind == "techniques":
            sections.append(("Sub-techniques", ["- **%s**" % ref(s) for s in sorted(subs[sid], key=lambda s: ids[s]["_aid"])]))
            sections.append(("Mitigations", bullets([x for x in ins if x[0] == "mitigates"])))
            det = [x for x in ins if x[0] == "detects" and kind_of(x[1]) == "detection"]
            det_lines = []
            for _, s, text in sorted(det, key=lambda x: ids[x[1]]["_aid"]):
                desc = oneline(clean(ids[s].get("description"))) or text
                det_lines.append("- **%s**%s" % (ref(s), " — " + desc if desc else ""))
                det_lines += analytic_lines(ids[s])
            sections.append(("Detection strategies", det_lines))
            sections.append(("Procedure examples", bullets([x for x in ins if x[0] == "uses"], with_kind=True)))
        if kind == "mitigations":
            sections.append(("Techniques addressed", bullets([x for x in outs if x[0] == "mitigates"])))
        if kind in ("groups", "software", "campaigns"):
            uses = [x for x in outs if x[0] == "uses"]
            sections.append(("Techniques used", bullets([x for x in uses if kind_of(x[1]) == "techniques"])))
            if kind != "software":
                sections.append(("Software used", bullets([x for x in uses if kind_of(x[1]) == "software"])))
        if kind == "groups":
            sections.append(("Campaigns", bullets([x for x in ins if x[0] == "attributed-to"])))
        if kind == "campaigns":
            sections.append(("Attributed to", bullets([x for x in outs if x[0] == "attributed-to"])))
        if kind == "software":
            sections.append(("Used by", bullets([x for x in ins if x[0] == "uses"], with_kind=True)))
        for head, lines in sections:
            if lines:
                md += ["", "## " + head, ""] + lines

        folder = os.path.join(out, kind)
        os.makedirs(folder, exist_ok=True)
        name = "%s_%s.md" % (o["_aid"], slug(title(sid)))
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")
        counts[kind] += 1
    return dict(counts), version


analytics = {}
DOMAINS_BY_NAME = {dname: chain for dname, chain in DOMAINS.values()}

if __name__ == "__main__":
    counts, version = build(sys.argv[1], sys.argv[2])
    print("ATT&CK versions:", version)
    for k, v in sorted(counts.items()):
        print("%5d %s" % (v, k))
    print("%5d total" % sum(counts.values()))
