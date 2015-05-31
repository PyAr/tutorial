#!/usr/bin/env python3

# REQUIREMENTS:
# pip install feedparser

# This script checks if there is a newer tag than the specified in CURRENT_TAG

# File: ~/.python-tutorial-es
# [email]

# USERNAME = your username
# PASSWORD = your password here
# FROMADDR = from@address.com
# TOADDRS = to@address.com


# $ crontab -e
# @weekly nice -n 19 /home/humitos/.virtualenvs/check-python-tutorial/bin/python /home/humitos/src/check_python_tutorial.py --email


import os
import sys
import smtplib
import feedparser
import configparser
import subprocess

from email.mime.text import MIMEText

TAGS_URL = 'http://hg.python.org/cpython/tags'
CURRENT_TAG = 'v3.4.2rc1'
ATOM_URL = 'http://hg.python.org/cpython/atom-tags'

rss = feedparser.parse(ATOM_URL)
tags = rss['entries'][:5]


def download_uncompress_create_diff(bz2_url, rev):
    c = 'wget --content-disposition -c {}'.format(bz2_url + '/Doc/tutorial/')
    output = subprocess.check_output(c, shell=True)
    c = 'tar xvf cpython-{}.tar.bz2 -C /tmp --wildcards --no-anchored \'Doc/tutorial/*.rst\''.format(rev)
    output = subprocess.check_output(c, shell=True)
    c = 'mv /tmp/cpython-{}/Doc/tutorial/*.rst ~/src/tutorial/original'.format(rev)
    output = subprocess.check_output(c, shell=True)
    c = 'cd ~/src/tutorial && git diff'
    output = subprocess.check_output(c, shell=True)
    c = 'cd ~/src/tutorial && git reset --hard origin/master'
    subprocess.check_output(c, shell=True)

    return output.decode('utf-8')


def send_mail(tag, bz2_url, rev):
    # Send an email to my account
    conf = configparser.ConfigParser()
    try:
        conf.read(os.path.expanduser('~/.python-tutorial-es'))
    except IOError:
        print('You need a config file in ~/.python-tutorial-es')

    text = \
'''Please go to {} to check it out.

        wget -c {}
        tar xvf {}.tar.bz2 -C /tmp --wildcards --no-anchored 'Doc/tutorial/*.rst'
        mv /tmp/cpython-{}/Doc/tutorial/*.rst ~/Source/tutorial/original
        cd ~/Source/tutorial
        git diff

------------------

{}

    '''.format(TAGS_URL, bz2_url, rev, rev,
               download_uncompress_create_diff(bz2_url, rev))
    msg = MIMEText(text)
    msg['From'] = conf.get('email', 'FROMADDR')
    msg['To'] = conf.get('email', 'TOADDRS')
    subject = '[Python HG] There is a new tag: {tag}'.format(tag=tag)
    msg['Subject'] = subject

    # Credentials
    username = conf.get('email', 'USERNAME')
    password = conf.get('email', 'PASSWORD')

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()


def new_version_found(py_version, bz2_url, rev):
    print('A new tag of Python is available "{}" at {}' \
          .format(py_version, bz2_url))

    if '--email' in sys.argv:
        send_mail(py_version, bz2_url, rev)


if __name__ == '__main__':

    for tag in tags:
        py_version = tag.title
        bz2_url = tag.link.replace('/rev/', '/archive/') + '.tar.bz2'
        rev = bz2_url.split('/')[-1].split('.')[0]

        major, minor, rest = py_version.split('.')

        if major != 'v3':
            continue

        current_major, current_minor, current_rest = CURRENT_TAG.split('.')
        if int(minor) > int(current_minor):
            new_version_found(py_version, bz2_url, rev)
        elif int(minor) == int(current_minor):
            # Options: a, b, rc1, rc2. We can just simply compare the
            # strings and we will know which version is previous to
            # the other one.
            if rest != current_rest \
               and rest[0] != current_rest[0] \
               and rest[1:] > current_rest[1:]:
                    new_version_found(py_version, bz2_url, rev)
