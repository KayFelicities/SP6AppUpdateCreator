#!/bin/sh
date_now=`date +"%Y%m%d-%H%M%S"`
cp_dir=/mnt/usb/SP6logs_$date_now

usb_array="sda sda1 sda2 sdb sdb1 sdb2 sdc sdc1 sdc2 sdd sdd1 sdd2 sde sde1 sde2 sdf sdf1 sdf2"

for usb in ${usb_array};do
	usb_dev=/dev/$usb
	if [ -e $usb_dev ];then
		if [ ! -d /mnt/usb ];then
			mkdir /mnt/usb
		fi
		mount $usb_dev /mnt/usb
		if [ -e /mnt/usb/update.img ];then
			mkdir $cp_dir
			cp -R /media/data/log $cp_dir/data/
			cp -R /tmp/log $cp_dir/tmp/
			echo copy to $usb_dev
		fi
		umount /mnt/usb
	fi
done

rm /media/data/update/*

echo log copy done