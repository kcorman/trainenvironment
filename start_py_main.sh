logsuffix=`date +%s`
new_log_name="logs/app-${logsuffix}.log"
echo "Rotating log file app.log to ${new_log_name}"
mv logs/app.log "${new_log_name}"
python3 main.py > logs/app.log 2>&1
