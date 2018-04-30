=======
A6-MITM
=======

A6-MITM is a program which mutates packets using ENIP (Ethernet/IP) and CIP (Common Industrial Protocol) protocols. 

This project has been created to help analyzing the behavior of SWaT, a water treatment testbed built at SUTD (Singapore University of Technology and Design).


Requirements
============

Hardware

* Ubuntu OS
* Laptop with at least two network interfaces

Software

* Python 2.7
* Bridge Control (https://help.ubuntu.com/community/NetworkConnectionBridge)
* NetfilterQueue (https://github.com/kti/python-netfilterqueue)
* Scapy (http://www.secdev.org/projects/scapy/)
* Ethernet/IP dissectors for Scapy (https://github.com/scy-phy/scapy-cip-enip)


Setup
=====

1. Ensure the device is physically connected in the middle of two PLCs.
2. Edit start.sh to bridge the two network adaptors.
3. 