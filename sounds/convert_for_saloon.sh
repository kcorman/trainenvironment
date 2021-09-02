#!/bin/bash
fullfile=$1
filename="${fullfile%.*}" # Extract filename without extension
newname="${filename}.left.mp3" 
sox $fullfile $newname remix 1,2 0
mv $newname saloon/
echo "Successfully moved $newname into saloon/ directory"
