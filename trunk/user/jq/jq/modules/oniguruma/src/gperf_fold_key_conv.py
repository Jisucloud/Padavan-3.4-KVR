#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re

REG_LINE_GPERF = re.compile('#line .+gperf"')
REG_HASH_FUNC = re.compile('hash\s*\(register\s+const\s+char\s*\*\s*str,\s*register\s+unsigned\s+int\s+len\s*\)')
REG_STR_AT = re.compile('str\[(\d+)\]')
REG_RETURN_TYPE = re.compile('^const\s+int\s*\*')
REG_FOLD_KEY = re.compile('unicode_fold(\d)_key\s*\(register\s+const\s+char\s*\*\s*str,\s*register\s+unsigned\s+int\s+len\)')
REG_ENTRY = re.compile('\{".*?",\s*(-?\d+)\s*\}')
REG_IF_LEN = re.compile('if\s*\(\s*len\s*<=\s*MAX_WORD_LENGTH.+')
REG_GET_HASH = re.compile('(?:register\s+)?(?:unsigned\s+)?int\s+key\s*=\s*hash\s*\(str,\s*len\);')
REG_GET_CODE = re.compile('(?:register\s+)?const\s+char\s*\*\s*s\s*=\s*wordlist\[key\]\.name;')
REG_CODE_CHECK = re.compile('if\s*\(\*str\s*==\s*\*s\s*&&\s*!strncmp.+\)')
REG_RETURN_WL = re.compile('return\s+&wordlist\[key\];')
REG_RETURN_0 = re.compile('return 0;')

def parse_line(s, key_len):
    s = s.rstrip()

    r = re.sub(REG_LINE_GPERF, '', s)
    if r != s: return r
    r = re.sub(REG_HASH_FUNC, 'hash(OnigCodePoint codes[])', s)
    if r != s: return r
    r = re.sub(REG_STR_AT, 'onig_codes_byte_at(codes, \\1)', s)
    if r != s: return r
    r = re.sub(REG_RETURN_TYPE, 'int', s)
    if r != s: return r
    r = re.sub(REG_FOLD_KEY, 'unicode_fold\\1_key(OnigCodePoint codes[])', s)
    if r != s: return r
    r = re.sub(REG_ENTRY, '\\1', s)
    if r != s: return r
    r = re.sub(REG_IF_LEN, 'if (0 == 0)', s)
    if r != s: return r
    r = re.sub(REG_GET_HASH, 'int key = hash(codes);', s)
    if r != s: return r
    r = re.sub(REG_GET_CODE, 'int index = wordlist[key];', s)
    if r != s: return r
    r = re.sub(REG_CODE_CHECK,
               'if (index >= 0 && onig_codes_cmp(codes, OnigUnicodeFolds%d + index, %d) == 0)' % (key_len, key_len), s)
    if r != s: return r

    r = re.sub(REG_RETURN_WL, 'return index;', s)
    if r != s: return r
    r = re.sub(REG_RETURN_0, 'return -1;', s)
    if r != s: return r

    return s

def parse_file(f, key_len):
    print "/* This file was converted by gperf_fold_key_conv.py\n      from gperf output file. */"

    line = f.readline()
    while line:
        s = parse_line(line, key_len)
        print s
        line = f.readline()


# main
argv = sys.argv
argc = len(argv)

key_len = int(argv[1])
parse_file(sys.stdin, key_len)
