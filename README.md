Introduction
------------

Generate a hosts file for consumption by Ansible using the list of guests in
an oVirt/RHEV environment. Relies on and reports on guests with the QEMU guest
agent installed and available, other guests are ommitted from the result as are
those that are down when the script is run.

Usage
-----

usage: ovirt-hosts-generate.py [-h] [-l LOCATION] [-u USER] -p PASSWORD
                               [-K KEY_FILE] [-C CERT_FILE] [-A CA_FILE] [-I]

Automatically generateAnsible hosts file for all guests thatreport an IP
address.

optional arguments:
  -h, --help            show this help message and exit
  -l LOCATION, --location LOCATION
  -u USER, --user USER
  -p PASSWORD, --password PASSWORD
  -K KEY_FILE, --key-file KEY_FILE
  -C CERT_FILE, --cert-file CERT_FILE
  -A CA_FILE, --ca_file CA_FILE
  -I, --insecure

