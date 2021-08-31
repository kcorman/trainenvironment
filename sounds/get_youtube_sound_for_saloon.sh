youtube-dl -x --audio-format mp3 --output "$2" $1
sh convert_to_left_only.sh $2
