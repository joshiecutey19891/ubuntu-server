#!/bin/bash
# Server Monitoring Script
# This script monitors server resources and logs them

# Inefficient: Running multiple commands in a loop instead of once
while true; do
    # Inefficiency 1: Spawning new process for date in loop
    echo "Timestamp: $(date)" >> /var/log/server_monitor.log
    
    # Inefficiency 2: Multiple separate grep calls instead of single awk/parsing
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    mem_free=$(free | grep Mem | awk '{print $4}')
    mem_total=$(free | grep Mem | awk '{print $2}')
    mem_used=$(free | grep Mem | awk '{print $3}')
    
    # Inefficiency 3: Multiple disk usage calls
    disk_root=$(df -h / | tail -1 | awk '{print $5}')
    disk_home=$(df -h /home | tail -1 | awk '{print $5}')
    disk_var=$(df -h /var | tail -1 | awk '{print $5}')
    
    # Inefficiency 4: String concatenation in loop
    log_line=""
    log_line="${log_line}CPU: ${cpu_usage}% "
    log_line="${log_line}| Mem Used: ${mem_used} "
    log_line="${log_line}| Mem Free: ${mem_free} "
    log_line="${log_line}| Disk /: ${disk_root} "
    log_line="${log_line}| Disk /home: ${disk_home} "
    log_line="${log_line}| Disk /var: ${disk_var}"
    
    echo "$log_line" >> /var/log/server_monitor.log
    
    # Inefficiency 5: Checking for processes inefficiently
    for proc in apache2 nginx mysql postgresql; do
        ps aux | grep $proc | grep -v grep > /dev/null
        if [ $? -eq 0 ]; then
            echo "Process $proc is running" >> /var/log/server_monitor.log
        fi
    done
    
    # Inefficiency 6: Sleep in tight loop without proper interval management
    sleep 5
done
