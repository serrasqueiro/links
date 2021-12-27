#-*- coding: utf-8 -*-
# links.py  (c)2021  Henrique Moreira

"""
Sample work using zson Python library
"""

# pylint: disable=missing-function-docstring

from zson.idtable import IdTable
from zson.zdict import ZDict

REWRITE = 0
JSON_FNAME = "links.json"
IO_ENCODING = "ISO-8859-1"

BY_ORDER = (
    "!",
    "ted-talks=",
    "ted-talks-info",
)


def main():
    sample(JSON_FNAME, {"re-write": REWRITE})


def sample(fname:str, opts:dict) -> bool:
    encoding = IO_ENCODING
    tbl = IdTable(encoding=encoding)
    tbl.load(fname)
    new = NewDict(tbl.get(), name="links")
    tbl.inject(new)
    tbl.dump_sort(False)  # customized sort
    # Now dump
    print(tbl.dump())
    if opts["re-write"]:
        is_ok = tbl.save(fname + "~")
        return is_ok
    infos = build_infos(open(fname, "r", encoding=encoding).read(), fname, tbl)
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
    same_content = infos["same-content"]
    if not same_content:
        print(f'Warn: {fname}: the same content! File size: {infos["file-size"]}, Dump size: {infos["dump-size"]}')
    return same_content


def get_who(tbl:IdTable, a_id:int) -> str:
    try:
        item = tbl.get_by_key("ted-talks-info", a_id)
    except KeyError:
        item = None
    if not item:
        return ""
    who = item["Speakers"]
    return who


def build_infos(data:str, fname:str, tbl) -> dict:
    infos = {
        "same-content": data == tbl.dump() + "\n",
        "dump-size": len(tbl.dump() + "\n"),
        "file-size": len(data),
    }
    return infos


class NewDict(ZDict):
    """ Customized dictionary """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def items(self) -> list:
        by_key = []
        for substr in BY_ORDER:
            for key in sorted(self.get_dict()):
                if key.startswith(substr) and key not in by_key:
                    by_key.append(key)
        for key in sorted(self.get_dict()):
            if key not in by_key:
                by_key.append(key)
        return self._items(str, by_key)


# Main script
if __name__ == "__main__":
    main()
