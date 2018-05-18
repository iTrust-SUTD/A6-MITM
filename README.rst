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
3. Edit mutate.py Line 202 with the incoming Ethernet interface.

Sample Execution
================


.. csv-table:: Mutation Table
   :header: "Name", "Code", "Description"
   :widths: 35, 20, 50

   "Add static Delta", "ASD(𝛿)", "Adds/subtracts an absolute, unchanging 𝛿 to state measurements"
   "Add Limits Delta", "ALD(𝛿)", "Adds/subtracts random value between -𝛿 and +𝛿 to state measurements"
   "Add Random Delta 𝛿", "ARD(𝛿\ :sub:`1`\,𝛿\ :sub:`2`\)", "Adds/subtracts a random value between 𝛿\ :sub:`1`\ and 𝛿\ :sub:`2`\ to state measurements"
   "Set to Zero", "STZ", "Sets state measurement to zero"
   "Set to One", "STO", Sets state measurement to one"
   "Set to Static", "STS(𝛿)", "Sets state measurement to static value"
   "Set to Random", "STR(𝛿\ :sub:`1`\,𝛿\ :sub:`2`\)", "Set state measurement to a random value between 𝛿\ :sub:`1`\ and 𝛿\ :sub:`2`\"
   "Bit Shift Left", "BSL(𝛿)", "Sets state measurement is bit-shifted to left by 𝛿 bits"
   "Bit Shift Right", "BSR(𝛿)", "Sets state measurement is bit-shifted to right by 𝛿 bits"