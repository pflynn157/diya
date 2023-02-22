#!/bin/bash

echo "Installing..."

INSTALL_PATH=/usr/share/diya

mkdir -p $INSTALL_PATH
cp src/creator.py $INSTALL_PATH
cp src/diya.py $INSTALL_PATH
cp src/generator.py $INSTALL_PATH
cp src/markdown.py $INSTALL_PATH
cp src/processor.py $INSTALL_PATH

mkdir -p $INSTALL_PATH/base
cp -r ./base/* $INSTALL_PATH/base

cp src/diya.sh /usr/bin/diya
chmod 777 /usr/bin/diya

echo "Done"

