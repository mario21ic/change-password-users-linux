#!/usr/bin/env python

import pwd
import string
from random import choice
import csv


def list_users():
    users = []
    for p in pwd.getpwall():
        if "/home/" in p.pw_dir and p.pw_uid >= 1000:
            users.append(p.pw_name)
    return users

def generate_password(length):
    return ''.join(choice("1234567890" + string.letters + string.digits + '_-.$') for _ in range(length))

def change_pass(user, password):
    return True

def write_csv(data):
    with open('report.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)

def main():
    users = list_users()
    data = []
    for user in users:
        password = generate_password(16)
        if change_pass(user, password):
            data.append([user, password])
    write_csv(data)

if __name__ == "__main__":
    main()
