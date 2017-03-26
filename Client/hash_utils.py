#!/usr/bin/python

import hashlib

def compute_hash(s):
    o = hashlib.sha1(s)
    return o.hexdigest()


if __name__ == '__main__':
    s = "GuruDarshan"
    print compute_hash(s)
