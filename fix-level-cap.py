import re, sys

# ── player.h: FixedVector<int,27> → vector<int> ──────────────
with open('dcss-src/source/player.h') as f:
    h = f.read()

print('player.h action_count line:')
for line in h.split('\n'):
    if 'action_count' in line:
        print(' ', line.strip())

fixed_h = h.replace('FixedVector<int, 27>', 'vector<int>', 1)
if fixed_h != h:
    with open('dcss-src/source/player.h', 'w') as f:
        f.write(fixed_h)
    print('player.h patched OK')
else:
    print('WARNING: FixedVector<int, 27> not found in player.h - searching...')
    for line in h.split('\n'):
        if 'FixedVector' in line and 'action' in line.lower():
            print(' ', line.strip())

# ── chardump.cc: count_action anzeigen und patchen ───────────
with open('dcss-src/source/chardump.cc') as f:
    cc = f.read()

m = re.search(r'void count_action\b[^\{]*\{.*?\n\}', cc, re.DOTALL)
if m:
    print('\ncount_action implementation:')
    print(m.group(0))
else:
    print('count_action not found in chardump.cc - full function search:')
    lines = cc.split('\n')
    for i, line in enumerate(lines):
        if 'count_action' in line and 'void' in line:
            print('\n'.join(lines[i:i+30]))
