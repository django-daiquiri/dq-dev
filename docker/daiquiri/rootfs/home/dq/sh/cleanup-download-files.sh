#!/bin/bash

if [ -d "$QUERY_DOWNLOAD_DIR" ]; then
find $QUERY_DOWNLOAD_DIR \
	-type f \
	'(' -name "*.csv" -o -name "*.fits" -o -name "*.xml"  -o -name "*.zip" ')' \
	-mtime +14 \
	-delete
fi

