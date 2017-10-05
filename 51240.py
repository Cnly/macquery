#! /usr/bin/env python3

import sys
import requests
import re

pattern = re.compile(r'<td bgcolor="#FFFFFF" align="center" style="font-size:16px;">(.*)</td>')

def anonymise(mac: str) -> str:
    '''
    Replace the last latter half of a MAC address with zeros
    '''
    result = ''
    if len(mac) == 17:
        # With delimiters
        for i in range(0, 7, 3):
            result += mac[i:i+2]
    elif len(mac) == 12:
        # Without delimiters
        result = mac[:7]
    else:
        print('Wrong format: {}'.format(mac))
        return None

    result += '000000'
    return result

def lookup(mac: str) -> str:
    amac = anonymise(mac)
    if not amac:
        return None
    response = requests.get('https://mac.51240.com/{}__mac/'.format(amac))
    text = response.text
    ret = [x.group(1) for x in pattern.finditer(text)]
    if ret[0] == '私营':
        print('Not found: {}'.format(mac))
        return None
    return ' | '.join(ret)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Put in MAC addresses as parameters.')
        exit(1)
    macs = sys.argv[1:]
    for mac in macs:
        ret = lookup(mac)
        if ret:
            print('{} | {}'.format(mac, ret))

