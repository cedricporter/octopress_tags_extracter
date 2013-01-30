#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
# Extract tags from Octopress's posts

import sys
import re
import os


def extract(filename):
    head = ""
    with open(filename) as file:
        state = 'init'
        for line in file.readlines():
            if state == 'init':
                if line.startswith("---"):
                    state = 'in'
            elif state == 'in':
                if line.startswith("---"):
                    break
                head += line
    tags = set()
    for line in head.splitlines():
        for m in re.findall("^tags: (.*?)$", line.strip()):
            if m.startswith('['):
                raw_tags = m[1:-1]
                for tag in raw_tags.split(", "):
                    tags.add(tag)

    for line in head.splitlines():
        for m in re.findall("^- (.*?)$", line.strip()):
            tags.add(m)

    return tags

if __name__ == '__main__':
    tags = set()

    for r, d, f in os.walk(sys.argv[1]):
        for file in f:
            if file.endswith(".markdown"):
                filename = os.path.join(r, file)
                tags.update(extract(filename))

    for tag in tags:
        if tag.strip():
            print tag
