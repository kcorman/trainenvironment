#!/bin/bash
fullfile=$1
filename="${fullfile%.*}" # Extract filename without extension
sox $fullfile "${filename}.right.mp3" remix 0 1,2
