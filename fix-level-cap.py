import re, sys

# ── player.h: FixedVector<int,27> → vector<int> ──────────────
with open('dcss-src/source/player.h') as f:
    h = f.read()

print('player.h action_count:')
for line in h.split('\n'):
    if 'action_count' in line:
        print(' ', line.strip())

fixed_h = h.replace('FixedVector<int, 27>', 'vector<int>', 1)
if fixed_h != h:
    with open('dcss-src/source/player.h', 'w') as f:
        f.write(fixed_h)
    print('player.h patched OK')
else:
    print('WARNING: FixedVector<int, 27> not found in player.h')

# ── chardump.cc: .init(0) → .assign(get_max_xl(), 0) ────────
with open('dcss-src/source/chardump.cc') as f:
    cc = f.read()

# Zeige den Kontext um die init() Zeile
lines = cc.split('\n')
for i, line in enumerate(lines):
    if 'action_count' in line and 'init' in line:
        print(f'\nchardump.cc line {i+1}: {line.strip()}')
        print('Context:')
        print('\n'.join(lines[max(0,i-5):i+10]))

# Fix: .init(0) → .assign(you.get_max_xl(), 0)
fixed_cc = cc.replace(
    'you.action_count[pair].init(0)',
    'you.action_count[pair].assign(you.get_max_xl(), 0)'
)

# Fallback: generisches .init(0) auf action_count
fixed_cc = re.sub(
    r'(action_count\[[^\]]+\])\.init\(0\)',
    r'\1.assign(you.get_max_xl(), 0)',
    fixed_cc
)

if fixed_cc != cc:
    with open('dcss-src/source/chardump.cc', 'w') as f:
        f.write(fixed_cc)
    print('\nchardump.cc patched OK')
else:
    print('\nWARNING: .init(0) pattern not found in chardump.cc')
    # Zeige alle action_count Zeilen zur Diagnose
    for i, line in enumerate(lines):
        if 'action_count' in line:
            print(f'  {i+1}: {line.strip()}')
