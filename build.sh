#!/bin/bash

tsc && tsc-alias

REPLACE="../../../web/"
WITH="../../"

SOURCE_DIR="./web"

# Replace all occurences of ../../../web with ../../ in .js files in the SOURCE_DIR
find $SOURCE_DIR -type f -name "*.js" -exec sed -i "s#$REPLACE#$WITH#g" {} \;

rm -r "./web/web"
mv ./web/custom_nodes/python-interpreter-node/web/python-interpreter-node.js ./web
rm -r web/custom_nodes