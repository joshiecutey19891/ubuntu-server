#!/bin/bash
# Optimized Server Monitoring Script
# This script monitors server resources efficiently

LOG_FILE="/var/log/server_monitor.log"
INTERVAL=5

monitor_once() {
    # Optimization 1: Single date call, stored in variable
    local current_timestamp
    current_timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Optimization 2: Parse all memory stats in single awk pass
    local memory_total_kb memory_used_kb memory_free_kb
    read -r memory_total_kb memory_used_kb memory_free_kb <<< "$(free | awk '/Mem:/ {print $2, $3, $4}')"
    
    # Optimization 3: Single df call for all mount points, parse with awk
    local disk_usage_root_percent disk_usage_home_percent disk_usage_var_percent
    read -r disk_usage_root_percent disk_usage_home_percent disk_usage_var_percent <<< "$(df -h / /home /var 2>/dev/null | awk 'NR>1 {gsub(/%/,"",$5); print $5}' | xargs)"
    
    # Optimization 4: Improved CPU usage calculation with single top call
    cpu_usage_percent=$(top -bn1 | awk '/^%Cpu/ {print 100-$8}')
    
    # Optimization 5: Use pgrep for efficient process checking
    local running_processes_list=""
    for process_name in apache2 nginx mysql postgresql; do
        if pgrep -x "$process_name" > /dev/null 2>&1; then
            running_processes_list+="$process_name "
        fi
    done
    
    # Optimization 6: Single printf for efficient string formatting
    printf "[%s] CPU: %.1f%% | Mem: %s/%s (%s free) | Disk /: %s%% /home: %s%% /var: %s%% | Running: %s\n" \
        "$current_timestamp" "$cpu_usage_percent" "$memory_used_kb" "$memory_total_kb" "$memory_free_kb" \
        "$disk_usage_root_percent" "$disk_usage_home_percent" "$disk_usage_var_percent" "${running_processes_list:-none}" >> "$LOG_FILE"
}

# Optimization 7: Calculate next execution based on start time to avoid drift
main_loop() {
    while true; do
        local monitoring_start_time
        monitoring_start_time=$(date +%s)
        
        monitor_once
        
        # Calculate time taken and adjust sleep
        local monitoring_end_time
        monitoring_end_time=$(date +%s)
        local elapsed_seconds=$((monitoring_end_time - monitoring_start_time))
        local remaining_sleep_time=$((INTERVAL - elapsed_seconds))
        
        # Sleep only if there's time left in the interval
        if [ $remaining_sleep_time -gt 0 ]; then
            sleep $remaining_sleep_time
        fi
    done
}

# Only run if executed directly (not sourced)
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main_loop
fi
