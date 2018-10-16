#!/bin/sh
mkdir -p target
tar czf target/ambulance-app.w2p -C src .
echo "application built"
