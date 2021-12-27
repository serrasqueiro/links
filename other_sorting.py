#-*- coding: utf-8 -*-
# other_sorting.py  (c)2021  Henrique Moreira

"""
Illustrate how customized sorting may look alike
"""

# pylint: disable=missing-function-docstring

from collections import OrderedDict


def main():
    adict = {"monday": 10, "thursday": 12, "wednesday": 34}
    sample(adict)


def customsort(dict1, key_order:list):
    """ taken from
	https://stackoverflow.com/questions/12031482/custom-sorting-python-dictionary
    """
    items = [dict1[k] if k in dict1.keys() else 0 for k in key_order]
    sorted_dict = OrderedDict()
    for i in range(len(key_order)):
        sorted_dict[key_order[i]] = items[i]
    return sorted_dict


def sample(dict1:dict):
    key_order = ["monday" ,"tuesday" ,"wednesday" ,"thursday" ,"friday" ,"saturday"]
    sorted_dicti = customsort(dict1, key_order)
    print(sorted_dicti)
    print("--" * 20, "List is:")
    for item, value in sorted_dicti.items():
        print(item, "; is:", value)
    print("--" * 20, "Sorted list:")
    print(sorted(sorted_dicti, key=str))


# Main script
if __name__ == "__main__":
    main()
