#!/bin/bash
fullfile=$1
filename="${fullfile%.*}" # Extract filename without extension
sox $fullfile "${filename}.left.mp3" remix 1,2 0
