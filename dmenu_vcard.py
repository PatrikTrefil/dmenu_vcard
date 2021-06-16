#!/usr/bin/env python3

import vobject
import os
import subprocess
import unidecode
import argparse
import sys

if len(sys.argv) == 2:
    directory_arg = sys.argv[1]

query_inp = subprocess.run(["dmenu", "-i", "-p", "Query:"], input=b"tel\nemail",
                           stdout=subprocess.PIPE, check=True).stdout.decode("UTF-8")[:-1]
if query_inp == "":
    exit(1)


def squeeze_string(text: str) -> str:
    """replaces multiple whitespaces with one and trims the string"""
    return " ".join(text.split())


def remove_accent(text: str) -> str:
    """removes special characters"""
    return unidecode.unidecode(text)


def get_query(card, query) -> list:
    """extracts queried information from card"""
    if query == "email":
        return card.email_list
    elif query == "tel":
        return card.tel_list


def copy_to_clipboard(text: str) -> None:
    """copies given text to user clipboard"""
    subprocess.run(["xclip", "-selection", "clipboard"],
                   input=text.encode("UTF-8"), check=True)


def load_info_names(DIRECTORY, query) -> (str, dict):
    info = {}
    names = ""
    for contact in os.listdir(DIRECTORY):
        with open(DIRECTORY + contact, "r") as vcard:
            card = vobject.readOne(vcard.read())
            card_name = squeeze_string(str(card.n.valueRepr()))
            card_name = remove_accent(card_name)
            try:
                card_name += f" ({squeeze_string(str(card.nickname.valueRepr()))})"
            except AttributeError:
                pass

            try:
                info[card_name] = get_query(card, query)
            except AttributeError:
                pass
            names += card_name + "\n"
    return names, info


def main(DIRECTORY, query):
    names, info = load_info_names(DIRECTORY, query)
    name = subprocess.run(["dmenu", "-i"], input=names.encode("UTF-8"),
                          stdout=subprocess.PIPE, check=True).stdout.decode("UTF-8")[:-1]

    if name in info.keys():
        if len(info[name]) == 1:
            res = info[name][0].valueRepr()
        else:
            DELIM = ":"
            options = [item.params["TYPE"][0] + DELIM + item.valueRepr()
                       for item in info[name]]
            string = "\n".join(options)
            res = subprocess.run(["dmenu", "-i"], input=string.encode("UTF-8"),
                                 stdout=subprocess.PIPE, check=True).stdout.decode("UTF-8")[:-1]
            res = res.split(":")[-1]
        copy_to_clipboard(res)


if __name__ == "__main__":
    main(directory_arg, query_inp)
