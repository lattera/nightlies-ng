#!/usr/bin/env zsh

jails=("9-stable_amd64")
configdir="/tank/poudriere/configs"
portstree="local"
jail_dataset="tank/poudriere/jails"
mydate=$(date '+%F_%T')
publishdir="/tank/poudriere/packages"

if [ ${portstree} = "default" ]; then
    sudo poudriere ports -u
fi

for j in ${jails}; do
    sudo poudriere bulk -f ${configdir}/${j}.ports.txt -j ${j} -p ${portstree}
    if [ ${?} -eq 0 ]; then
        sudo rsync -a $(zfs get -H -ovalue mountpoint ${jail_dataset})/data/packages/${j}-${portstree}/ ${publishdir}/${j}
    fi
done
