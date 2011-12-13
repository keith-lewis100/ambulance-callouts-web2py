#!/bin/sh
mkdir -p target
svn export src target/temp
tar czf target/ambulance-app.w2p -C target/temp .
echo "application built"
