#!/bin/bash

DEB=diya_0.1.0-0_amd64

mkdir -p $DEB/DEBIAN
mkdir -p $DEB/usr/share/diya/base
mkdir -p $DEB/usr/bin

cp -r DEBIAN/* $DEB/DEBIAN
cp -r base/* $DEB/usr/share/diya/base
cp -r src/*.py $DEB/usr/share/diya
cp -r src/diya.sh $DEB/usr/bin/diya

chmod 777 $DEB/usr/bin/diya

echo "Done"

