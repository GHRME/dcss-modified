import re, os, subprocess

# ── 1. Datei mit count_action finden ──────────────────────────
result = subprocess.run(
    ['grep', '-rl', 'void count_action', 'dcss-src/source/'],
    capture_output=True, text=True
)
files = result.stdout.strip().split('\n')
print("Files with count_action:", files)

target = None
for f in files:
    if f.strip():
        target = f.strip()
        break

if not target:
    print("ERROR: count_action not found in any source file!")
    exit(1)

print(f"\n=== count_action in: {target} ===")
with open(target, 'r') as f:
    content = f.read()

# Funktion extrahieren und anzeigen
match = re.search(r'void count_action\b[^{]*\{(.+?)(?=\n\w)', content, re.DOTALL)
if match:
    func_text = match.group(0)[:1500]
    print(func_text)
else:
    # Zeige einfach 40 Zeilen ab count_action
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'void count_action' in line:
            print('\n'.join(lines[i:i+40]))
            break

# ── 2. Fix anwenden ───────────────────────────────────────────
original = content

# Fix A: ASSERT/ASSERTM über action.size() vs get_max_xl()
content = re.sub(
    r'ASSERTM?\s*\([^;]*\.size\s*\(\)[^;]*get_max_xl[^;]*\)\s*;',
    'if ((int)action.size() < you.get_max_xl()) action.resize(you.get_max_xl(), 0); // patched',
    content
)

# Fix B: assign(27, 0) → assign(you.get_max_xl(), 0)
content = re.sub(
    r'\.assign\s*\(\s*27\s*,',
    '.assign(you.get_max_xl(),',
    content
)

# Fix C: assign(MAX_XP_LEVEL, ...) → assign(you.get_max_xl(), ...)
content = re.sub(
    r'\.assign\s*\(\s*MAX_XP_LEVEL\s*,',
    '.assign(you.get_max_xl(),',
    content
)

# Fix D: Prüfe ob XL-Index (arg < 27) oder ähnlich
content = re.sub(
    r'ASSERTM?\s*\([^;]*arg\s*<\s*27\s*[^;]*\)\s*;',
    'ASSERT(arg >= 0 && arg < 99); // patched level cap',
    content
)

# Fix E: xl < 27 Assertion
content = re.sub(
    r'ASSERTM?\s*\([^;]*xl\s*<\s*27\s*[^;]*\)\s*;',
    'ASSERT(xl >= 0 && xl < 99); // patched level cap',
    content
)

if content != original:
    with open(target, 'w') as f:
        f.write(content)
    print("\nFix applied!")
else:
    print("\nWARNING: No known pattern matched. Showing all action-related lines:")
    for i, line in enumerate(content.split('\n')):
        stripped = line.strip().lower()
        if 'action' in stripped and any(x in stripped for x in ['size', 'assign', 'assert', 'resize', '27', 'max_xl']):
            print(f"  Line {i+1}: {line.strip()}")
