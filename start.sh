ifconfig br0 down

brctl delbr br0
brctl addbr br0
brctl stp br0 off

# ifconfig br0 up

brctl addif br0 enp0s3
brctl addif br0 enp0s8

# ifconfig br0 down

ifconfig enp0s3 0 0.0.0.0
ifconfig enp0s8 0 0.0.0.0
ifconfig br0 192.168.1.125 netmask 255.255.255.0 up