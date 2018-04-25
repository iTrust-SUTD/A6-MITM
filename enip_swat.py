# -*- coding: utf-8 -*-
# Copyright (c) 2015 David I. Urbina, david.urbina@utdallas.edu
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
"""Scapy Dissector for Ethernet/IP Implicit I/O messages of PLC 1."""
from scapy import all as scapy_all

import enip_tcp
import cip

__all__ = ['SWAT_TAGS','SWAT_LIT','SWAT_P1_ALL','SWAT_MV','SWAT_FIT', 'SWAT_AIT', 'SWAT_P']
    
class SWAT_TAGS(scapy_all.Packet):
    name = 'SWAT_TAGS'

    TAG_CODES = {
        0xa002b3a2: "HMI_MV",
        0xa002e1e2: "HMI_FIT",
        0xa0020cb9: "HMI_LIT",
        0xa0020cb9: "HMI_AIT",
        0xa0020cb9: "HMI_P"
    }

    fields_desc = [
        scapy_all.BitEnumField('tag', 0, 32, TAG_CODES)                                     
    ]                       

class SWAT_LIT(scapy_all.Packet):
    name = 'SWAT_LIT'
    fields_desc = [
        scapy_all.LEIntField('Pv', 0),
        scapy_all.LEIntField('Heu', 0),
        scapy_all.LEIntField('Leu', 0),
        scapy_all.LEIntField('SALL', 0),
        scapy_all.LEIntField('SAL', 0),
        scapy_all.LEIntField('SAH', 0),
        scapy_all.LEIntField('SAHH', 0),
        # scapy_all.LEIntField('Spare3', 0),
        scapy_all.BitEnumField('spare1', 0, 1, {}),
        scapy_all.BitEnumField('control', 0, 1, {0: 'actual', 1: 'simulation'}),
        scapy_all.BitEnumField('status', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('WiFi', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('ALL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AHH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.X3BytesField('Spare2', 0),
        scapy_all.LEIntField('Sim_Pv', 0)

    ]                 

class SWAT_FIT(scapy_all.Packet):
    name = 'SWAT_FIT'
    fields_desc = [
        scapy_all.LEIntField('Pv', 0),
        scapy_all.LEIntField('Heu', 0),
        scapy_all.LEIntField('Leu', 0),
        scapy_all.LEIntField('SALL', 0),
        scapy_all.LEIntField('SAL', 0),
        scapy_all.LEIntField('SAH', 0),
        scapy_all.LEIntField('SAHH', 0),
        scapy_all.LEIntField('Totaliser', 0),
        scapy_all.BitEnumField('status', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('Rst_Totaliser', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('WiFi', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('control', 0, 1, {0: 'actual', 1: 'simulation'}),
        scapy_all.BitEnumField('ALL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AHH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.X3BytesField('Spare', 0),
        scapy_all.LEIntField('Sim_Pv', 0),
        scapy_all.LEIntField('Spare2', 0)

    ]      

class SWAT_AIT(scapy_all.Packet):
    name = 'SWAT_AIT'
    fields_desc = [        
        scapy_all.LEIntField('Pv', 0),
        scapy_all.LEIntField('Heu', 0),
        scapy_all.LEIntField('Leu', 0),
        scapy_all.LEIntField('SALL', 0),
        scapy_all.LEIntField('SAL', 0),
        scapy_all.LEIntField('SAH', 0),
        scapy_all.LEIntField('SAHH', 0),
        scapy_all.BitEnumField('status', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('Rst_Totaliser', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('WiFi', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('control', 0, 1, {0: 'actual', 1: 'simulation'}),
        scapy_all.BitEnumField('ALL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('AHH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.X3BytesField('Spare', 0),
        scapy_all.LEIntField('Sim_Pv', 0),

    ]            

class SWAT_P1_ALL(scapy_all.Packet):
    name = 'SWAT_P1_ALL'
    fields_desc = [
        scapy_all.LEIntField('FIT101_Pv', 0),
        scapy_all.LEIntField('LIT101_Pv', 0),
        scapy_all.ByteField('spare3', 0),
        scapy_all.ByteField('spare4', 0),
        scapy_all.ByteEnumField('P101_cmd', 0, {1: 'off', 2: 'on'}),
        scapy_all.ByteField('spare5', 0),
        scapy_all.ByteEnumField('P102_cmd', 0, {1: 'off', 2: 'on'}),
        scapy_all.ByteField('spare6', 0),
        scapy_all.ByteField('spare7', 0),
        scapy_all.ByteField('spare8', 0),
        scapy_all.BitEnumField('FIT101_status', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('FIT101_Rst_Totaliser', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('FIT101_WiFi', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FIT101_control', 0, 1, {0: 'actual', 1: 'simulation'}),
        scapy_all.BitEnumField('FIT101_ALL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FIT101_AL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FIT101_AH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FIT101_AHH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.ByteField('spare9', 0),
        scapy_all.LEIntField('FIT101_H', 0),
        scapy_all.LEIntField('FIT101_HH', 0),
        scapy_all.LEIntField('FIT101_L', 0),
        scapy_all.LEIntField('FIT101_LL', 0),
        scapy_all.BitEnumField('LIT101_spare', 0, 1, {}),
        scapy_all.BitEnumField('LIT101_control', 0, 1, {0: 'actual', 1: 'simulation'}),
        scapy_all.BitEnumField('LIT101_status', 0, 1, {0: 'unhealthy', 1: 'healthy'}),
        scapy_all.BitEnumField('LIT101_WiFi', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('LIT101_ALL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('LIT101_AL', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('LIT101_AH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('LIT101_AHH', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.LEIntField('LIT101_SALL', 0),
        scapy_all.LEIntField('LIT101_SAL', 0),
        scapy_all.LEIntField('LIT101_SAH', 0),
        scapy_all.LEIntField('LIT101_SAHH', 0),
        scapy_all.BitEnumField('spare10', 0, 1, {}),
        scapy_all.BitEnumField('spare11', 0, 1, {}),
        scapy_all.BitEnumField('spare12', 0, 1, {}),
        scapy_all.BitEnumField('MV101_Avl', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('MV101_FTC', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('MV101_FTO', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('MV101_Auto', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('MV101_Reset', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.ByteEnumField('MV101_status', 0, {1: 'off', 2: 'on'}),
        scapy_all.ByteField('spare13', 0),
        scapy_all.ByteField('spare14', 0),
        scapy_all.ByteEnumField('P101_status', 0, {1: 'off', 2: 'on'}),
        scapy_all.X3BytesField('Spare', 0),
        scapy_all.LEIntField('spare15', 0),
        scapy_all.LEIntField('spare16', 0),
        scapy_all.LEIntField('spare17', 0),
        scapy_all.LEIntField('spare18', 0),
        scapy_all.LEIntField('P101_RunHr', 0),
        scapy_all.LEIntField('P101_RunHr2', 0),
        scapy_all.ByteField('spare19', 0),
        scapy_all.ByteField('spare20', 0),
        scapy_all.LEIntField('P101_Permissive', 0),
        scapy_all.LEIntField('spare21', 0)
        # scapy_all.ByteField('spare4', 0),
        # scapy_all.LEIntField('spare', 0),
        # scapy_all.LEIntField('LIT101_Sim_Pv', 0),
        # scapy_all.ByteField('spare4', 0),
        # scapy_all.ByteField('spare5', 0),
        # scapy_all.LEIntField('P102_RunHr', 0),
        # scapy_all.LEIntField('P102_RunHr', 0),
        # scapy_all.ByteField('spare4', 0),
        # scapy_all.ByteField('spare5', 0),
        # scapy_all.LEIntField('P102_Permissive', 0),
        # scapy_all.LEIntField('spare', 0)
    ]  

class SWAT_MV(scapy_all.Packet):
    name = 'SWAT_MV'
    fields_desc = [
        scapy_all.ByteEnumField('cmd', 0, {1: 'closed', 2: 'open'}),
        scapy_all.ByteField('spare2', 0),
        scapy_all.ByteEnumField('status', 0, {1: 'closed', 2: 'open'}),
        scapy_all.ByteField('spare3', 0),
        scapy_all.BitEnumField('spare4', 0, 1, {}),
        scapy_all.BitEnumField('spare5', 0, 1, {}),
        scapy_all.BitEnumField('spare6', 0, 1, {}),
        scapy_all.BitEnumField('Avl', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FTC', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FTO', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Auto', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Reset', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.X3BytesField('Spare7', 0)
    ] 

class SWAT_P(scapy_all.Packet):
    name = 'SWAT_P'
    fields_desc = [
        scapy_all.ByteEnumField('cmd', 0, {1: 'closed', 2: 'open'}),
        scapy_all.ByteField('spare2', 0),
        scapy_all.ByteEnumField('status', 0, {1: 'closed', 2: 'open'}),
        scapy_all.ByteField('spare3', 0),
        scapy_all.LEIntField('RunMin', 0),
        scapy_all.LEIntField('Total_RunMin', 0),
        scapy_all.LEIntField('RunHr', 0),
        scapy_all.LEIntField('Total_RunHr', 0),
        scapy_all.LEIntField('Permissive', 0),
        scapy_all.LEIntField('Shutdown', 0),
        scapy_all.LEIntField('SD', 0),
        scapy_all.BitEnumField('Avl', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Fault', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Auto', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Remote', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FTS', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('FTR', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Reset_RunHr', 0, 1, {0: 'disable', 1: 'enable'}),
        scapy_all.BitEnumField('Reset', 0, 1, {0: 'disable', 1: 'enable'}),
    ] 
                                                                  
scapy_all.bind_layers(cip.CIP, SWAT_TAGS, service=0x4c)
# scapy_all.bind_layers(SWAT_TAGS, SWAT_P1_ALL, tag=256)
scapy_all.bind_layers(SWAT_TAGS, SWAT_LIT, tag=0xa0020cb9)
scapy_all.bind_layers(SWAT_TAGS, SWAT_MV, tag=0xa002b3a2)
scapy_all.bind_layers(SWAT_TAGS, SWAT_AIT, tag=0xa0020cb9)
scapy_all.bind_layers(SWAT_TAGS, SWAT_FIT, tag=0xa002e1e2)
scapy_all.bind_layers(SWAT_TAGS, SWAT_P, tag=0xa0022ad6)