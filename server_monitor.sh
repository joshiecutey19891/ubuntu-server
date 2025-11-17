#!/bin/bash
# Server Monitoring Script
# This script monitors server resources and logs them

# Inefficient: Running multiple commands in a loop instead of once
while true; do
    # Inefficiency 1: Spawning new process for date in loop
    echo "Timestamp: $(date)" >> /var/log/server_monitor.log
    
    # Inefficiency 2: Multiple separate grep calls instead of single awk/parsing
    cpu_usage_percent=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    memory_free_kb=$(free | grep Mem | awk '{print $4}')
    memory_total_kb=$(free | grep Mem | awk '{print $2}')
    memory_used_kb=$(free | grep Mem | awk '{print $3}')
    
    # Inefficiency 3: Multiple disk usage calls
    disk_usage_root_percent=$(df -h / | tail -1 | awk '{print $5}')
    disk_usage_home_percent=$(df -h /home | tail -1 | awk '{print $5}')
    disk_usage_var_percent=$(df -h /var | tail -1 | awk '{print $5}')
    
    # Inefficiency 4: String concatenation in loop
    monitoring_log_entry=""
    monitoring_log_entry="${monitoring_log_entry}CPU: ${cpu_usage_percent}% "
    monitoring_log_entry="${monitoring_log_entry}| Mem Used: ${memory_used_kb} "
    monitoring_log_entry="${monitoring_log_entry}| Mem Free: ${memory_free_kb} "
    monitoring_log_entry="${monitoring_log_entry}| Disk /: ${disk_usage_root_percent} "
    monitoring_log_entry="${monitoring_log_entry}| Disk /home: ${disk_usage_home_percent} "
    monitoring_log_entry="${monitoring_log_entry}| Disk /var: ${disk_usage_var_percent}"
    
    echo "$monitoring_log_entry" >> /var/log/server_monitor.log
    
    # Inefficiency 5: Checking for processes inefficiently
    for process_name in apache2 nginx mysql postgresql; do
        ps aux | grep $process_name | grep -v grep > /dev/null
        if [ $? -eq 0 ]; then
            echo "Process $process_name is running" >> /var/log/server_monitor.log
        fi
    done
    
    # Inefficiency 6: Sleep in tight loop without proper interval management
    sleep 5
done
