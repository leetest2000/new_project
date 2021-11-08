#!/usr/bin/python3

import sys
import os
from datetime import datetime, date, time, timedelta
import csv
import re
import random
import string
import getpass
import pprint
import socket
#import jinja2
import ipaddress # load in the ipaddress module
import smtplib
import subprocess
import paramiko
import difflib
import getpass

# For debugging
import logging as lg
#lg.basicConfig(level=lg.DEBUG)

# colours
from colorama import Fore, Back, Style

# for SNMP
#from pysnmp.entity.rfc3413.oneliner import cmdgen
# Create command generator object
#cmdGen = cmdgen.CommandGenerator()

# define snmp parameters
SNMP_HOST = ''
SNMP_PORT = 161
SNMP_COMMUNITY = ''

# Set indent for pprint
pp = pprint.PrettyPrinter(indent=4)


# Set user/pass
#user = getpass.getuser()
#pwd = getpass.getpass()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()

def backup_junipers():
# read a file with the host devices... need split else it will put one letter on a line at a time.
       file2 = open('juniper_devices.txt','r')
       host_targets = file2.read().split("\n")
       #print(host_targets)
       file2.close()

       total = 0

       for host in host_targets:
            now = str(datetime.now())
            now = now.replace(' ',',')
            tday = now.split(',')
                yesterday = str(datetime.now() - timedelta(1))
                yesterday = yesterday.replace(' ',',')
                yday = yesterday.split(',')
                #total = total + '\n===============================================================================================================================\n'
                if len(host) == 0:
                        continue
                print((Fore.RED + "============================ " + Style.RESET_ALL + "Backup of " + host + Fore.RED + " =================================" + Style.RESET_ALL))
                ssh.connect(host)
                ssh.exec_command('set cli screen-length 0')
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show configuration | display set')
                output = ssh_stdout.read()
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show configuration')
                output2 = ssh_stdout.read()

                for text in output:
                        file = open('/home/law/PY/jun_bkp_conf/' + host + '_%s_set.cfg' % tday[0], 'a')
                        file.write(text)

                for text in output2:
                        file = open('/home/law/PY/jun_bkp_conf/' + host + '_%s.cfg' % tday[0], 'a')
                        file.write(text)

#               print(output)
                file_today = ('/home/law/PY/jun_bkp_conf/' + host + '_%s.cfg' % tday[0])
                file_yday = ('/home/law/PY/jun_bkp_conf/' + host + '_%s.cfg' % yday[0])

def backup_cumulus():
        # read a file with the host devices... need split else it will put one letter on a line at a time.
        file2 = open('cumulus_devices.txt','r')
        host_targets = file2.read().split("\n")
        #print(host_targets)
        file2.close()

        total = 0

        for host in host_targets:
                now = str(datetime.now())
                now = now.replace(' ',',')
                tday = now.split(',')
                yesterday = str(datetime.now() - timedelta(1))
                yesterday = yesterday.replace(' ',',')
                yday = yesterday.split(',')
                #total = total + '\n===============================================================================================================================\n'
                if len(host) == 0:
                        continue
                print((Fore.RED + "============================ " + Style.RESET_ALL + "Backup of " + host + Fore.RED + " =================================" + Style.RESET_ALL))
                ssh.connect(host)
            #    ssh.exec_command('net show configuration commands')
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('net show configuration commands')
                output = ssh_stdout.read()
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('net show config files')
                output2 = ssh_stdout.read()

                for text in output:
                        file = open('/home/law/PY/cu_bkp_conf/' + host + '_%s_set.cfg' % tday[0], 'a')
                        file.write(text)

                for text in output2:
                        file = open('/home/law/PY/cu_bkp_conf/' + host + '_%s.cfg' % tday[0], 'a')
                        file.write(text)

#               print(output)
                file_today = ('/home/law/PY/cu_bkp_conf/' + host + '_%s.cfg' % tday[0])
                file_yday = ('/home/law/PY/cu_bkp_conf/' + host + '_%s.cfg' % yday[0])

print('\nsaving cumulus to /home/law/PY/cu_bkp_conf/\n')
backup_cumulus()

print('\nsaving junipers to /home/law/PY/jun_bkp_conf/\n')
backup_junipers()
  
