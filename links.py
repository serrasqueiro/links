#-*- coding: utf-8 -*-
# links.py  (c)2021  Henrique Moreira

"""
Sample work using zson Python library
"""

# pylint: disable=missing-function-docstring

from zson.idtable import IdTable

REWRITE = 0
JSON_FNAME = "links.json"


def main():
    sample(JSON_FNAME, {"re-write": REWRITE})


def sample(fname:str, opts:dict):
    tbl = IdTable(encoding="iso-8859-1")
    tbl.load(fname)
    print(tbl.dump())
    if opts["re-write"]:
        is_ok = tbl.save(fname + "~")
        return is_ok
    refs = tbl.get_one("ted-talks-info")
    assert refs
    is_ok = tbl.index("ted-talks-info")
    assert is_ok
    key, talks = tbl.get_one_key("ted-talks")
    print("=" * 20)
    for item in talks:
        a_id, a_key, a_mark, a_title = item["Id"], item["Key"], item["Mark"], item["Title"]
        if a_id <= 0:
            continue
        url = key[key.index("=")+1:].replace("$1", a_key)
        who = get_who(tbl, a_id)
        xtra = f"By: {who}\n" if who else ""
        if a_mark is None:
            a_mark = "-"
        print(f"""
<li>{a_id:<6} {a_mark:<20} <a href="{url}" _target="_blank">{a_title}</a>
{xtra}</li>
""")
    print("=" * 20)
    return True


def get_who(tbl:IdTable, a_id:int) -> str:
    try:
        item = tbl.get_by_key("ted-talks-info", a_id)
    except KeyError:
        item = None
    if not item:
        return ""
    who = item["Speakers"]
    return who


# Main script
if __name__ == "__main__":
    main()
