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
   :widths: 30, 20, 50

   "Add static Delta", "ASD", "Adds/subtracts an absolute, unchanging $\delta$ to state measurements"
   "Smith", "John, Junior"


 & ASD($\delta$) & Adds/subtracts an absolute, unchanging $\delta$ to state measurements & ASD(500) $\Rightarrow$ Before: LIT101=300 After: LIT101=800\\\hline
Add Limits Delta & ALD($\delta$) & Adds/subtracts random value between $-\delta$ and $+\delta$ to state measurements & ALD(10) $\Rightarrow$ Before: LIT101=300 After: LIT101=307\\\hline
Add Random Delta $\delta$ & ARD($\delta_1$,$\delta_2$) & Adds/subtracts a random value between $\delta_1$ and $\delta_2$ to state measurements & ARD(100, 200) $\Rightarrow$  Before: LIT101=300 After: LIT101=450\\\hline
Set to Zero & STZ & Sets state measurement to zero& STZ $\Rightarrow$ Before: LIT101=300 After: LIT101=0\\\hline
Set to One & STO &Sets state measurement to one& STO $\Rightarrow$ Before: LIT101=300 After: LIT101=1\\\hline
Set to Static &STS($\delta$) & Sets state measurement to static value& STS(756) $\Rightarrow$ Before: LIT101=300 After: LIT101=756\\\hline
Set to Random & STR($\delta_1$,$\delta_2$) & Set state measurement to a random value between $\delta_1$ and $\delta_2$ & STR(100, 200) $\Rightarrow$ Before: LIT101=300 After: LIT101=179\\\hline
Bit Shift Left &BSL($\delta$) & Sets state measurement is bit-shifted to left by $\delta$ bits& BSL(4) $\Rightarrow$ Before: LIT101=300 After: LIT101=5982.85\\\hline
Bit Shift Right &BSR($\delta$) & Sets state measurement is bit-shifted to right by $\delta$ bits & BSR(4) $\Rightarrow$ Before: LIT101=300 After: LIT101=3356044.00\\\hline