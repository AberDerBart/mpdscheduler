#!/bin/bash


sed "s/WHICH_MPDSCHEDULER/$(which mpdScheduler|sed 's/\//\\\//g')/" < mpdScheduler.service >/etc/systemd/system/mpdScheduler.service

systemctl daemon-reload

echo 'installed systemd service, run'
echo
echo '$ systemctl start mpdScheduler'
echo
echo 'to run mpdScheduler, or'
echo
echo '$ systemctl enable mpdScheduler'
echo 
echo 'to run it at every boot'
