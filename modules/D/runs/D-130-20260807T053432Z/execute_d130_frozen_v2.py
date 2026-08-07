from pathlib import Path

source = Path(__file__).with_name('execute_d130_frozen.py')
code = source.read_text(encoding='utf-8')
old = "g=float(spec['transport_derivation']['gap_g_C']); a=float(spec['transport_derivation']['edge_rate_a']); p0=np.array(spec['state_space']['initial_population'],float); u=np.ones(3)/3; Tend=1/g; tp=math.log(2)/(2*g); M=np.array(spec['transport_derivation']['parent_matrix'],float)"
new = "g=float(spec['transport_derivation']['gap_g_C']); a=float(spec['transport_derivation']['edge_rate_a']); p0=np.array(spec['state_space']['initial_population'],float); u=np.ones(3)/3; Tend=float(spec['execution_interval']['t_span'][1]); tp=math.log(2)/(2*g); M=np.array(spec['transport_derivation']['parent_matrix'],float)"
if old not in code:
    raise SystemExit('expected frozen-interval implementation line not found')
code = code.replace(old, new, 1)
old_replay = "cg=float(cs['transport_derivation']['gap_g_C']); cpp=np.array(cs['state_space']['initial_population']); recon=u+math.exp(-cg*(1/cg))*(cpp-u); replay_err=float(np.max(np.abs(recon-baseline)))"
new_replay = "cg=float(cs['transport_derivation']['gap_g_C']); cpp=np.array(cs['state_space']['initial_population']); replay_end=float(cs['execution_interval']['t_span'][1]); recon=u+math.exp(-cg*replay_end)*(cpp-u); replay_err=float(np.max(np.abs(recon-baseline)))"
if old_replay not in code:
    raise SystemExit('expected clean-replay interval line not found')
code = code.replace(old_replay, new_replay, 1)
exec(compile(code, str(source), 'exec'))
