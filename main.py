#!/usr/bin/env python

import ConfigParser
import pwd
import string
from random import choice
import os
import subprocess
from subprocess import PIPE,Popen
import csv
import ConfigParser


config = ConfigParser.ConfigParser()
config.read("config.ini")
uid_start = config.getint("settings", "uid_start")
uid_end = config.getint("settings", "uid_end")


def list_users():
    users = []
    for p in pwd.getpwall():
        if (p.pw_uid in range(uid_start, uid_end)) \
                and "/home/" in p.pw_dir:
            users.append(p.pw_name)
    return users

def generate_password(length):
    return ''.join(choice(string.letters + string.digits + '_-.$') for _ in range(length))

def change_pass(user, password):
    echo_process = Popen(["echo", user+":"+password], stdout=PIPE)
    chpasswd_process = Popen(["chpasswd"], stdin=echo_process.stdout, stdout=PIPE, stderr=PIPE)
    echo_process.stdout.close()
    output = chpasswd_process.communicate()[0]
    chpasswd_process.stdout.close()
    if output=='':
        return True
    return False

def write_csv(data):
    with open('report.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)

def main():
    data = []
    for user in list_users():
        password = generate_password(16)
        if change_pass(user, password):
            data.append([user, password])
    write_csv(data)

if __name__ == "__main__":
    main()
