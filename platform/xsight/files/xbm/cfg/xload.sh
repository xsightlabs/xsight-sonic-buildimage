# debug_level=1 - Error
# 2 - Notice
# 3 - Info
# 4 - Debug
# 5 - Debug with Packet trace
sudo insmod /home/admin/xbm/cfg/xpci.ko attach_if="xcpu" num_of_ports=16 debug_level=3 netdev_mode=1

echo "echo 3 > /sys/module/xpci/parameters/debug_level"
echo 3 > /sys/module/xpci/parameters/debug_level
