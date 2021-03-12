#!/bin/sh

FILE="all_api.apib"
if [ -e $FILE ]; then
  rm -rf all_api.apib
fi
cat *.apib > all_api.apib