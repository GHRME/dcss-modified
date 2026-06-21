import re, subprocess

# ── player.h: FixedVector<int,27> → vector<int> ──────────────
with open('dcss-src/source/player.h') as f:
    h = f.read()
fixed_h = h.replace('FixedVector<int, 27>', 'vector<int>', 1)
if fixed_h != h:
    with open('dcss-src/source/player.h', 'w') as f:
        f.write(fixed_h)
    print('player.h: FixedVector<int,27> → vector<int> OK')
else:
    print('WARNING: pattern not found in player.h')

# ── Alle .cc Dateien: .init(0) auf action_count → .assign() ──
result = subprocess.run(
    ['grep', '-rl', 'action_count', 'dcss-src/source/'],
    capture_output=True, text=True
)
files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip().endswith('.cc')]

for path in files:
    with open(path) as f:
        content = f.read()
    fixed = re.sub(
        r'(you\.action_count\[[^\]]+\])\.init\(0\)',
        r'\1.assign(you.get_max_xl(), 0)',
        content
    )
    if fixed != content:
        with open(path, 'w') as f:
            f.write(fixed)
        print(f'{path}: .init(0) → .assign(get_max_xl(), 0) OK')

print('Done.')
