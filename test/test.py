#-*- coding: utf-8 -*-
# test.py  (c)2022  Henrique Moreira

""" Sample test using ztab module (Python library)
"""

# pylint: disable=missing-function-docstring

import sys
import os.path
import ztab


def main():
    parse_args(sys.argv[1:])


def parse_args(args):
    param = args if args else ["links.json"]
    is_ok = tester(param)
    assert is_ok


def tester(args):
    opts = {
        "verbose": 0,
    }
    param = args
    if param[0] == "-v":
        opts["verbose"] += 1
        del param[0]
    for item in param:
        is_ok = do_test(item, opts)
        if not is_ok:
            print("Failed:", item)
    return True


def do_test(fname:str, opts=None) -> bool:
    """ Do the test on json file 'fname'
    """
    if opts is None:
        opts = {}
    verbose = int(opts.get("verbose")) if "verbose" in opts else 1
    name = os.path.basename(fname)
    if name.endswith(".json"):
        name = name[:-len(".json")]
    json_fname = fname
    tbl = ztab.tobject.DTable(name)
    assert tbl.get_name() == name, fname
    tbl = ztab.tobject.DTable(name)
    is_ok = tbl.load(json_fname)
    assert is_ok
    alist = tbl.obj()
    print("Loaded:", name)
    assert len(alist) == 1, "Since original file is dict, I have expected len==1"
    there = alist[0]
    key, item = "", []
    talks = (None, None)
    talk_infos = (None, None)
    for key in sorted(there):
        item = there[key]
        if verbose > 0:
            print(key, ":", item, end="\n\n")
        else:
            print("# KEY:", key)
        if key.startswith("ted-talks="):
            assert talks[0] is None
            talks = (key, item)
        elif key in ("ted-talks-info"):
            talk_infos = (key, item)
    assert key == "~", key
    assert item
    here = item[0]
    assert here["Id"] == -1
    assert here["Key"] == "*"
    assert not here["Title"]
    show_talks(talks, talk_infos)
    #tbl.save_as_list(fname + "~")
    return True

def show_talks(talks, talk_infos):
    print("\n# " + talks[0], end=":\n\n")
    key, whot = talk_infos
    idxa = {}
    for talk in whot:
        an_id = talk["Id"]
        idxa[an_id] = talk
    talk = None
    for talk in talks[1]:
        an_id = talk["Id"]
        if an_id == 0:
            continue
        print(talk, end="\n\n")
        speaker = idxa.get(an_id)
        assert speaker is not None, f"Could not find at 'ted-talks-info': {an_id}: {talk['Key']}"
        assert idxa[an_id]["Speakers"]
    assert talk is not None
    assert talk["Id"] == 0
    assert not talk["Key"]
    assert not talk["Title"]
    print("---")
    #print(idxa)


# Main script
if __name__ == "__main__":
    main()
