#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import argparse

PATTERN = re.compile("([^\s]+)\s+\((.+)\)\s+type: (.+)\s+default: (.+)")

BOOL_CHOICES = ["y", "n", "1", "0", "true", "false"]


def ParseFlag(flag):
    flag = flag.replace("\n", " ").strip()
    m = PATTERN.search(flag)
    return {k: v.strip()
            for k, v
            in zip(["name", "description", "type", "default"], m.groups())}


def ParseFlags(src):
    filename = src[:src.find("\n") - 1]

    res = []
    for flag in src.split("    -")[1:]:
        flagobj = ParseFlag(flag)
        flagobj["filename"] = filename[filename.rfind("/") + 1:]
        res.append(flagobj)
    return res


def GetProg(lines):
    return lines[:lines.find(":")]


if __name__ == '__main__':
    lines = "".join(sys.stdin.readlines())

    prog = GetProg(lines)

    lines = lines[lines.find("Flags from"):]

    flags = []
    for a in lines.split("Flags from")[1:]:
        flags = flags + ParseFlags(a)

    TYPEMAP = dict(
        int32=int,
        int64=int,
        string=str,
        double=float,
        bool=bool)

    parser = argparse.ArgumentParser(prog=prog, description="hoge")
    for flag in flags:
        if flag["name"] == "help":
            continue
        parser.add_argument(
            "--" + flag["name"],
            default=flag["default"],
            type=TYPEMAP[flag["type"]],
            # choices=BOOL_CHOICES if flag["type"] == "bool" else None,
            # nargs=None if flag["type"] == "bool" else "?",
            help="{description}".format(**flag))
    parser.print_help()
