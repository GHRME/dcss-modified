import re, sys, os

filepath = 'dcss-src/source/god-conduct.cc'
with open(filepath, 'r') as f:
    content = f.read()

# Show count_action function for diagnostics
match = re.search(r'void count_action[^{]*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', content)
if match:
    print("=== count_action ===")
    print(match.group(0)[:1000])
else:
    print("count_action not found in god-conduct.cc")

# Fix 1: Replace ASSERT that checks action.size() == get_max_xl()
# This fails when loading old saves where vectors were sized to 27
fixed = re.sub(
    r'(ASSERTM?\([^;]*\.size\(\)[^;]*get_max_xl\(\)[^;]*\);)',
    r'// Modified: resize instead of assert to support level cap changes\n    if ((int)action.size() < you.get_max_xl()) action.resize(you.get_max_xl(), 0);',
    content
)

# Fix 2: If vectors initialized with hard-coded 27 instead of get_max_xl()
if fixed == content:
    fixed = re.sub(
        r'action\.assign\(27\b',
        'action.assign(you.get_max_xl()',
        content
    )

if fixed != content:
    print("Applied fix to god-conduct.cc")
    with open(filepath, 'w') as f:
        f.write(fixed)
else:
    print("WARNING: No matching pattern found - manual inspection needed")
    # Print more context for debugging
    for i, line in enumerate(content.split('\n')):
        if 'action' in line.lower() and ('size' in line or 'assign' in line or 'assert' in line.lower()):
            print(f"  Line {i+1}: {line.strip()}")
