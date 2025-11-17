# Quick Reference: Inefficient vs Optimized Code Patterns

This guide provides quick examples of common performance anti-patterns and their optimized versions.

## Pattern 1: File Reading

### ❌ Inefficient - Load entire file into memory
```python
with open(file, 'r') as f:
    all_lines = f.readlines()
for line in all_lines:
    process(line)
```

### ✅ Optimized - Stream line by line
```python
with open(file, 'r') as f:
    for line in f:
        process(line.rstrip('\n'))
```

**Impact**: 90%+ memory reduction for large files

---

## Pattern 2: Multiple Data Passes

### ❌ Inefficient - Multiple iterations
```python
for line in lines:
    if 'ERROR' in line:
        errors.append(line)

for line in lines:
    if 'WARNING' in line:
        warnings.append(line)
```

### ✅ Optimized - Single pass
```python
for line in lines:
    if 'ERROR' in line:
        errors.append(line)
    elif 'WARNING' in line:
        warnings.append(line)
```

**Impact**: 2-3x faster processing

---

## Pattern 3: String Concatenation

### ❌ Inefficient - String += in loop
```python
result = ""
for item in items:
    result += str(item) + "\n"
```

### ✅ Optimized - List join or f-strings
```python
# Option 1: List join
parts = [str(item) for item in items]
result = '\n'.join(parts)

# Option 2: Modern f-string
result = '\n'.join(f"{item}" for item in items)
```

**Impact**: 10x faster for 1000+ items

---

## Pattern 4: Nested Loop Duplicates

### ❌ Inefficient - O(n²) nested loops
```python
duplicates = []
for i in range(len(items)):
    for j in range(i+1, len(items)):
        if items[i] == items[j]:
            if items[i] not in duplicates:
                duplicates.append(items[i])
```

### ✅ Optimized - Counter O(n)
```python
from collections import Counter
counter = Counter(items)
duplicates = [item for item, count in counter.items() if count > 1]
```

**Impact**: 100x+ faster for 1000+ items

---

## Pattern 5: Regex in Loop

### ❌ Inefficient - Compile on every iteration
```python
for line in lines:
    match = re.search(r'ERROR\s+(\d+)', line)
    if match:
        process(match.group(1))
```

### ✅ Optimized - Pre-compile regex
```python
pattern = re.compile(r'ERROR\s+(\d+)')
for line in lines:
    match = pattern.search(line)
    if match:
        process(match.group(1))
```

**Impact**: 10x+ faster for large datasets

---

## Pattern 6: Multiple Directory Walks

### ❌ Inefficient - Multiple os.walk() calls
```python
# First pass for files
files = []
for root, dirs, filenames in os.walk(directory):
    files.extend([os.path.join(root, f) for f in filenames])

# Second pass for sizes
sizes = {}
for root, dirs, filenames in os.walk(directory):
    for f in filenames:
        path = os.path.join(root, f)
        sizes[path] = os.path.getsize(path)
```

### ✅ Optimized - Single walk with stat
```python
files = []
sizes = {}
for root, dirs, filenames in os.walk(directory):
    for f in filenames:
        path = os.path.join(root, f)
        files.append(path)
        sizes[path] = os.stat(path).st_size
```

**Impact**: 2x faster, better cache locality

---

## Pattern 7: Chunked File Reading

### ❌ Inefficient - Load entire file
```python
with open(file, 'rb') as f:
    data = f.read()
    checksum = hashlib.md5(data).hexdigest()
```

### ✅ Optimized - Process in chunks
```python
md5 = hashlib.md5()
with open(file, 'rb') as f:
    while chunk := f.read(8192):
        md5.update(chunk)
checksum = md5.hexdigest()
```

**Impact**: Can handle files larger than available RAM

---

## Pattern 8: Shell Process Spawning

### ❌ Inefficient - Multiple grep calls
```bash
mem_total=$(free | grep Mem | awk '{print $2}')
mem_used=$(free | grep Mem | awk '{print $3}')
mem_free=$(free | grep Mem | awk '{print $4}')
```

### ✅ Optimized - Single call with multiple outputs
```bash
read mem_total mem_used mem_free <<< $(free | awk '/Mem:/ {print $2, $3, $4}')
```

**Impact**: 66% fewer process spawns

---

## Pattern 9: Process Checking

### ❌ Inefficient - ps with grep
```bash
ps aux | grep apache2 | grep -v grep
```

### ✅ Optimized - Use pgrep
```bash
pgrep -x apache2
```

**Impact**: Cleaner, faster, fewer processes

---

## Pattern 10: Directory Scanning

### ❌ Inefficient - listdir with stat
```python
for name in os.listdir(directory):
    path = os.path.join(directory, name)
    if os.path.isdir(path):
        size = os.path.getsize(path)
```

### ✅ Optimized - Use os.scandir()
```python
for entry in os.scandir(directory):
    if entry.is_dir():
        size = entry.stat().st_size
```

**Impact**: 2-3x faster, fewer syscalls

---

## Pattern 11: File Comparison

### ❌ Inefficient - Byte-by-byte reading
```python
with open(f1, 'rb') as file1, open(f2, 'rb') as file2:
    while True:
        b1 = file1.read(1)
        b2 = file2.read(1)
        if b1 != b2:
            return False
        if not b1:
            return True
```

### ✅ Optimized - Use filecmp
```python
import filecmp
return filecmp.cmp(f1, f2, shallow=False)
```

**Impact**: 1000x+ faster, optimized C implementation

---

## Pattern 12: Dictionary Updates

### ❌ Inefficient - Check then update
```python
if key not in dict:
    dict[key] = []
dict[key].append(value)
```

### ✅ Optimized - Use defaultdict
```python
from collections import defaultdict
dict = defaultdict(list)
dict[key].append(value)
```

**Impact**: Cleaner, slightly faster

---

## Pattern 13: Timing Loops

### ❌ Inefficient - Fixed sleep (drift)
```bash
while true; do
    process_data
    sleep 5
done
```

### ✅ Optimized - Compensate for execution time
```bash
while true; do
    start=$(date +%s)
    process_data
    elapsed=$(($(date +%s) - start))
    sleep $((5 - elapsed))
done
```

**Impact**: Prevents timing drift over long runs

---

## Pattern 14: Data Filtering

### ❌ Inefficient - Multiple filters
```python
result = []
for item in items:
    if condition1(item):
        result.append(item)

filtered = []
for item in result:
    if condition2(item):
        filtered.append(item)
```

### ✅ Optimized - Combined filter or comprehension
```python
filtered = [item for item in items 
           if condition1(item) and condition2(item)]
```

**Impact**: Single pass, more readable

---

## Pattern 15: Path Operations

### ❌ Inefficient - String concatenation
```python
path = directory + '/' + subdir + '/' + filename
if os.path.exists(path):
    size = os.path.getsize(path)
```

### ✅ Optimized - Use pathlib
```python
from pathlib import Path
path = Path(directory) / subdir / filename
if path.exists():
    size = path.stat().st_size
```

**Impact**: More portable, cleaner, object-oriented

---

## General Principles

1. **Minimize I/O operations** - Read/write once, not multiple times
2. **Stream when possible** - Don't load everything into memory
3. **Single-pass algorithms** - Process data once, not multiple times
4. **Right data structures** - Set for lookups, Counter for frequency, etc.
5. **Pre-compile patterns** - Regex, templates outside of loops
6. **Batch operations** - Group related operations together
7. **Use stdlib** - Python/system libraries are optimized in C
8. **Profile first** - Measure before and after optimization
9. **Error handling** - Don't let exceptions kill performance
10. **Cache appropriately** - Remember expensive calculations when safe

---

## Tools for Performance Analysis

### Python
```bash
# Profile with cProfile
python -m cProfile -s cumtime script.py

# Memory profiling
python -m memory_profiler script.py

# Line profiler
kernprof -l -v script.py
```

### Shell
```bash
# Time execution
time ./script.sh

# Monitor resources
top -p $(pgrep script.sh)
htop -p $(pgrep script.sh)

# Trace system calls
strace -c ./script.sh
```

### General
```bash
# I/O statistics
iostat -x 1

# Network monitoring
iftop
nethogs
```
