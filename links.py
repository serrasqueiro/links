#-*- coding: utf-8 -*-
# links.py  (c)2021  Henrique Moreira

"""
Sample work using zson Python library
"""

# pylint: disable=missing-function-docstring

import sys
from zson.idtable import IdTable
from zson.znewdict import NewDict


REWRITE = 0
JSON_FNAME = "links.json"
IO_ENCODING = "ISO-8859-1"

BY_ORDER = (
    "!",
    "youtube-cool=",
    "youtube-cool-info",
    "ted-talks=",
    "ted-talks-info",
    "curiosity-stream=",
    "curiosity-stream-info",
)

BY_ORDER_AUTHORS = (
    "!",
    "ted-speakers",
)


def main():
    parse_args(sys.argv[1:])


def parse_args(args):
    if args:
        io_file = args[0]
        assert len(args) == 1
    else:
        io_file = JSON_FNAME
    byorder = BY_ORDER if "links" in io_file else BY_ORDER_AUTHORS
    sample(io_file, {"re-write": REWRITE, "byorder": byorder})


def sample(fname:str, opts:dict) -> bool:
    encoding = IO_ENCODING
    byorder = opts["byorder"]
    tbl = IdTable(encoding=encoding)
    is_ok = tbl.load(fname)
    if not is_ok:
        print("Cannot read:", fname)
        return False
    # TEST - even if key is not ordered alphabetically, result is!
    #tbl._table["~"].append({"Id": 7, "Key": "Seven", "Title": "What", "Case": "sample"})
    ###
    new = NewDict(byorder, tbl.get(), name="links")
    tbl.inject(new)
    tbl.dump_sort(False)  # customized sort
    tbl.ensure_ascii(False)	# allow e.g. ISO-8859-1 chars (Latin-1)
    # Now dump
    print(tbl.dump())
    if int(opts["re-write"]) == 1:
        is_ok = tbl.save(fname, ensure_ascii=False)
        return is_ok
    infos = build_infos(open(fname, "r", encoding=encoding).read(), tbl)
    print("=" * 20)
    subitems = []
    for subitem in byorder:
        if subitem.endswith("="):
            subitem = subitem[:-1]
            subitems.append((subitem, subitem + "-info"))
    for subitem, subitem_info in subitems:
        html_raw(tbl, "h2", item=subitem, info=subitem_info)
    print("=" * 20)
    same_content = infos["same-content"]
    if not same_content:
        print(f'Warn: {fname}: not the same content!',
              f'File size: {infos["file-size"]}, Dump size: {infos["dump-size"]}')
    return same_content


def html_raw(tbl, *args, **kwargs):
    if not args:
        h_level = "h2"
    else:
        h_level = args[0]
    h_levels = (f"<{h_level}>", f"</{h_level}>")
    item = kwargs["item"]
    info = kwargs["info"]  # e.g. ted-talks-info
    refs = tbl.get_one(info)
    assert refs
    is_ok = tbl.index(info)
    assert is_ok
    key, talks = tbl.get_one_key(item)
    pre = f"\n<!-- {item} {len(talks)-1} item(s); info='{info}' -->\n"
    print(f"{pre}{h_levels[0]}{item}{h_levels[1]}")
    for item in talks:
        a_id, a_key, a_mark, a_title = item["Id"], item["Key"], item["Mark"], item["Title"]
        if a_id <= 0:
            continue
        url = key[key.index("=")+1:].replace("$1", a_key)
        who = get_who(tbl, info, a_id)
        xtra = f"By: {who}\n" if who else ""
        if a_mark is None:
            a_mark = "-"
        print(f"""
<li>{a_id:<6} {a_mark:<20} <a href="{url}" _target="_blank">{a_title}</a>
{xtra}</li>
""".rstrip())


def get_who(tbl:IdTable, info:str, a_id:int) -> str:
    if not info:
        info = "ted-talks-info"
    try:
        item = tbl.get_by_key(info, a_id)
    except KeyError:
        item = None
    if not item:
        return ""
    who = item.get("Speakers")
    if not who:
        return ""
    return who


def build_infos(data:str, tbl) -> dict:
    astr = tbl.dump() + "\n"
    infos = {
        "same-content": data == astr,
        "dump-size": len(astr),
        "file-size": len(data),
    }
    return infos


# Main script
if __name__ == "__main__":
    main()
