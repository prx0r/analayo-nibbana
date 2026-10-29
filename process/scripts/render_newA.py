"""newA render driver — uniform rhythm (bell/Q/plain/Analayo, analayo-only)
-> build/audio_newA/ (seed + S1..S6 + full_newA_essay.mp3).

Usage: python3 process/scripts/render_newA.py [seed|s1|..|s6|all|full] [...]
  seed|s1..: render just those sections (fast iteration; cache hits elsewhere)
  all:        everything + full assembly (default when no args? no: default=seed)
  full:       reassemble full mp3 + manifest from existing section mp3s
Renders stay local-only, uncommitted (see .gitignore). Data + gates
keep Nibbana; speech says Nirvana (voice-time substitution).
"""
import sys

sys.path.insert(0, 'tools')
import render_a_essay as R

R.NEWA = True
R.P0_NO_BELLS = False  # bells ring in newA (uniform ritual)
args = [a for a in sys.argv[1:] if not a.startswith('-')]
if not args:
    args = ['seed']
ALL = ('seed', 's1', 's2', 's3', 's4', 's5', 's6')
if args == ['all']:
    args = list(ALL)
R.NEWA_SECTIONS = [a for a in args if a in ALL]
R.NEWA_ASSEMBLE_ONLY = (args == ['full'])
if R.NEWA_ASSEMBLE_ONLY:
    R.NEWA_SECTIONS = []
R.NEWA_SEED_ONLY = False  # section list drives now
R.main()
