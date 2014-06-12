#!/bin/bash

FULLIMPORT="http://localhost:8082/solr3/xplaycms/dataimport?command=full-import&clean=false=&wt=json"
CLEAN="http://localhost:8082/solr3/xplaycms/update"

function now() {
	date "+%Y-%m-%dT%H:%M:%Sz" -u
}

function thirty() {
	date "+%Y-%m-%dT%H:%M%Sz" -u -d"30 minutes ago"
}

function status() {
	STATUS=\"$(curl --silent -XGET http://localhost:8082/solr3/xplaycms/dataimport?command=status&wt=json)\"
	T=$(echo "${STATUS}" | grep 'idle')
	echo ${T}
}

while true; do
	for i in $(seq 1 5); do
		if [ $i -eq 5 ]; then
			exit 5
		fi
		echo ${i}
		echo $(now)
		echo $(thirty)
		echo $(status)
		sleep 10
	done
done

