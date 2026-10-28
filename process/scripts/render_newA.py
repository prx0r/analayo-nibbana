"""newA render driver — uniform rhythm (reader quote -> plain voice-2 ->
Analayo) -> build/audio_newA/ (seed + S1..S6 + full_newA_essay.mp3).

Usage: python3 process/scripts/render_newA.py [seed|all]
Renders stay local-only, uncommitted (see .gitignore). Data + gates
keep Nibbana; speech says Nirvana (voice-time substitution).
"""
import sys

sys.path.insert(0, 'tools')
import render_a_essay as R

R.NEWA = True
R.P0_NO_BELLS = False  # bells ring in newA (uniform ritual)
R.NEWA_SEED_ONLY = (len(sys.argv) < 2 or sys.argv[1] == 'seed')
R.main()
