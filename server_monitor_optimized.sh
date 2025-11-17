#!/bin/bash
# Optimized Server Monitoring Script
# This script monitors server resources efficiently

LOG_FILE="/var/log/server_monitor.log"
INTERVAL=5

monitor_once() {
    # Optimization 1: Single date call, stored in variable
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Optimization 2: Parse all memory stats in single awk pass
    read mem_total mem_used mem_free <<< $(free | awk '/Mem:/ {print $2, $3, $4}')
    
    # Optimization 3: Single df call for all mount points, parse with awk
    read disk_root disk_home disk_var <<< $(df -h / /home /var 2>/dev/null | awk 'NR>1 {gsub(/%/,"",$5); print $5}' | xargs)
    
    # Optimization 4: Improved CPU usage calculation with single top call
    cpu_usage=$(top -bn1 | awk '/^%Cpu/ {print 100-$8}')
    
    # Optimization 5: Use pgrep for efficient process checking
    local processes=""
    for proc in apache2 nginx mysql postgresql; do
        if pgrep -x "$proc" > /dev/null 2>&1; then
            processes+="$proc "
        fi
    done
    
    # Optimization 6: Single printf for efficient string formatting
    printf "[%s] CPU: %.1f%% | Mem: %s/%s (%s free) | Disk /: %s%% /home: %s%% /var: %s%% | Running: %s\n" \
        "$timestamp" "$cpu_usage" "$mem_used" "$mem_total" "$mem_free" \
        "$disk_root" "$disk_home" "$disk_var" "${processes:-none}" >> "$LOG_FILE"
}

# Optimization 7: Calculate next execution based on start time to avoid drift
main_loop() {
    while true; do
        local start_time=$(date +%s)
        
        monitor_once
        
        # Calculate time taken and adjust sleep
        local end_time=$(date +%s)
        local elapsed=$((end_time - start_time))
        local sleep_time=$((INTERVAL - elapsed))
        
        # Sleep only if there's time left in the interval
        if [ $sleep_time -gt 0 ]; then
            sleep $sleep_time
        fi
    done
}

# Only run if executed directly (not sourced)
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main_loop
fi
