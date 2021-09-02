logsuffix=`date +%s`
new_log_name="logs/app-${logsuffix}.log"
#LOG_FILE=logs/app.log
LOG_FILE=/dev/null
echo "Rotating log file app.log to ${new_log_name}"
mv logs/app.log "${new_log_name}"
python3 main.py > $LOG_FILE 2>&1
