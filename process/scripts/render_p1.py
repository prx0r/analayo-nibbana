"""p1 render driver — bells + sfx kit + YT anchor offsets -> build/audio_p1/.

Usage: python3 process/scripts/render_p1.py [seed|all]
  seed = seed only (proof: bowls + bells + direct essay-0 + Fish Qs)
  all  = seed + S1..S6 + full (aborts on L20 until per-window offsets, §69)

Taste gates are listen-side (Fish voice approval, sfx levels); this
script changes no data, only the render. Renders stay local-only,
uncommitted (see .gitignore).
"""
import sys

sys.path.insert(0, 'tools')
import render_a_essay as R

R.P1 = True
R.P0_NO_BELLS = False  # bells render (OUT is audio_p1 via P1, v1 stays frozen)
R.P1_SEED_ONLY = (len(sys.argv) < 2 or sys.argv[1] == 'seed')
R.main()
