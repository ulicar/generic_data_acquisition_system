#!/bin/bash

for proto in $(find . -iname \*.proto); do
	dir=$(dirname $proto)
	echo $dir $proto
	protoc -I/usr/include -I. --python_out=. $proto || exit 1
done

exit 0