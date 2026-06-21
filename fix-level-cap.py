import re, os, subprocess

# ── 1. Datei mit count_action finden ──────────────────────────
result = subprocess.run(
    ['grep', '-rl', 'count_action', 'dcss-src/source/'],
    capture_output=True, text=True
)
files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
print("Files with count_action:", files)

# Datei mit der Funktionsdefinition finden
target = None
for f in files:
    with open(f) as fh:
        if 'void count_action' in fh.read():
            target = f
            break

if not target:
    print("ERROR: count_action definition not found!")
    exit(1)

print(f"\n=== Patching: {target} ===")
with open(target, 'r') as f:
    content = f.read()

# Zeige die Funktion
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'void count_action' in line:
        print("Function content:")
        print('\n'.join(lines[i:i+35]))
        break

original = content

# Fix: Nach "action.assign(you.get_max_xl(), 0)" oder "action.assign(...)"
# einen resize-Zweig hinzufügen, damit alte Saves funktionieren.
# Muster: if (action.empty()) \n    action.assign(you.get_max_xl(), 0);
content = re.sub(
    r'(if\s*\(action\.empty\(\)\)\s*\n\s*action\.assign\(you\.get_max_xl\(\)\s*,\s*0\)\s*;)',
    r'\1\n    else if ((int)action.size() < you.get_max_xl()) action.resize(you.get_max_xl(), 0); // patched',
    content
)

# Fallback: assign mit Literal 27
content = re.sub(
    r'(if\s*\(action\.empty\(\)\)\s*\n\s*action\.assign\(\s*27\s*,\s*0\)\s*;)',
    r'if (action.empty() || (int)action.size() < you.get_max_xl())\n        action.resize(you.get_max_xl(), 0); // patched',
    content
)

# Fallback 2: assign auf einer Zeile (ohne Zeilenumbruch)
content = re.sub(
    r'(if\s*\(action\.empty\(\)\)\s*action\.assign\(you\.get_max_xl\(\)\s*,\s*0\)\s*;)',
    r'if (action.empty() || (int)action.size() < you.get_max_xl()) action.resize(you.get_max_xl(), 0); // patched',
    content
)

if content != original:
    with open(target, 'w') as f:
        f.write(content)
    print("\nFix applied successfully!")
else:
    print("\nWARNING: Pattern not matched. Showing all relevant lines:")
    for i, line in enumerate(lines):
        if any(x in line for x in ['action.', 'ASSERT', 'assign', 'resize', '.size()', 'empty()', 'get_max_xl']):
            print(f"  {i+1}: {line}")
