#!/bin/bash -e
if [ -e "./demo.zip" ] ; then
    rm ./demo.zip
fi

mkdir tmp
cp index.py tmp/
cd tmp
pip3 install -t . iotedge_application_link_sdk==0.0.3 #打包驱动SDK
zip -r demo.zip .
cd ..
cp tmp/demo.zip .
rm -rf tmp
