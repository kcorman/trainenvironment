youtube-dl -x --audio-format mp3 --output "%(uploader)s%(title)s.%(ext)s" $1 --exec "sh convert_for_saloon.sh {}"
