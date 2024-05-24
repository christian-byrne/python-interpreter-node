#!/bin/bash

tsc && tsc-alias

REPLACE="../../../web/"
WITH="../../"
NODE_NAME="python-interpreter-node"
SOURCE_DIR="./web"

# Replace all occurences of ../../../web with ../../ in .js files in the SOURCE_DIR
find $SOURCE_DIR -type f -name "*.js" -exec sed -i "s#$REPLACE#$WITH#g" {} \;

# Create list of all ts files in ./web (only in 1st level)
find ./web -maxdepth 1 -type f -name "*.ts" > ts_files.txt

# Convert to just the file name
sed -i 's/.*\///' ts_files.txt

# Replace all .ts with .js in ts_files.txt
sed -i 's/\.ts/\.js/' ts_files.txt

rm -r "./web/web"

# Move all compiled js files with mangled paths to ./web
while read line; do
    mv ./web/custom_nodes/$NODE_NAME/web/$line ./web
done < ts_files.txt

rm ts_files.txt
rm -r ./web/custom_nodes

# TODO: When building, remove .ts .js.map, .tsbuildinfo, console.logs|debug|info, python typing/types