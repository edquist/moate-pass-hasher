#!/usr/bin/python

import os
import csv
import sys
import string
import random
import crypt

_valid_chars = string.letters + string.digits
def randpass(passlen):
    return ''.join( random.choice(_valid_chars) for x in range(passlen) )

def gen_pass_hash(passlen):
    password = randpass(passlen)
    salt = randpass(16)
    pass_hash = crypt.crypt(password, "$6$rounds=131070$" + salt + "$")
    return password, pass_hash

def quote(s):
    return '"%s"' % s if "'" in s else "'%s'" % s

def csv2yaml(path, outyamlpath, outcsvpath, passlen):
    csvout = csv.writer(open(outcsvpath, "w"))
    csvout.writerow(["e-mail", "Name", "Period", "Username", "Password"])
    yamlout = open(outyamlpath, "w")
    print >>yamlout, "accounts:"
    print >>yamlout, "  users:"
    for email, name, period in csv.reader(open(path)):
        if '@' not in email:
            continue
        user, host = email.split('@')
        password, pass_hash = gen_pass_hash(passlen)
        csvout.writerow([email, name, period, user, password])
        print >>yamlout, "    %s:" % user
        print >>yamlout, "      comment : %s" % quote(period)
        print >>yamlout, "      email   : %s" % quote(email)
        print >>yamlout, "      fullname: %s" % quote(name)
        print >>yamlout, "      password: %s" % quote(pass_hash)
        print >>yamlout

def usage():
    print >>sys.stderr, ("usage: %s studentsList.csv out.yaml out.csv PASSLEN"
                         % os.path.basename(__file__))
    sys.exit(1)

def main(args):
    if len(args) != 4:
        usage()
    path, outyamlpath, outcsvpath = args[:3]
    passlen = int(args[3])
    csv2yaml(path, outyamlpath, outcsvpath, passlen)

if __name__ == '__main__':
    main(sys.argv[1:])

