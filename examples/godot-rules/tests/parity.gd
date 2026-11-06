extends SceneTree

var errors=[]
var checks=0

func compare(actual,expected,at):
	if expected is Dictionary:
		for key in expected:
			# Localized feedback text intentionally differs, game rules do not.
			if key=="message":continue
			if not actual.has(key):errors.append(at+" missing "+key)
			else:compare(actual[key],expected[key],at+"."+key)
	elif expected is Array:
		if actual.size()!=expected.size():errors.append(at+" array size")
		else:
			for i in range(expected.size()):compare(actual[i],expected[i],at+"["+str(i)+"]")
	elif expected is float or expected is int:
		if abs(float(actual)-float(expected))>0.000001:errors.append(at+" expected "+str(expected)+" got "+str(actual))
	elif actual!=expected:errors.append(at+" expected "+str(expected)+" got "+str(actual))

func _initialize():
	var sim=load("res://scripts/simulation.gd").new()
	var fixtures=JSON.parse_string(FileAccess.get_file_as_string("res://data/parity-fixtures.json"))
	for f in fixtures.fixtures:
		var s=f.initial.duplicate(true)
		for item in f.steps:
			for i in range(int(item.get("repeat",1))):sim.tick(s,item.input,item.dt,false)
		compare(s,f.expected,f.id);checks+=1
	# Retry never rerolls a template or removes acquired evidence.
	for seed_value in range(100):
		var a=sim.create_state(false,false,seed_value)
		var b=sim.create_state(true,true,seed_value)
		if a.template_id!=b.template_id or a.seed!=b.seed or not b.evidence:errors.append("retry seed "+str(seed_value))
	checks+=1
	# Both templates retain a long all-clear interval, with no simultaneous impacts.
	for t in sim.templates:
		var simultaneous=0;var longest=0;var safe=0
		for tick_index in range(480):
			var phases=[]
			for offset in t.offsets:phases.append(fposmod(tick_index/60.0+offset,4.0))
			if phases[0]>=3 and phases[0]<3.38 and phases[1]>=3 and phases[1]<3.38:simultaneous+=1
			if phases[0]<2 and phases[1]<2:safe+=1;longest=max(longest,safe)
			else:safe=0
		if simultaneous or longest<10:errors.append("unsafe template "+t.id)
	checks+=1
	var x=sim.create_state(false,false,0,"xiaomo")
	x.projectiles=[{"id":1,"x":5.0,"y":5.0,"vx":0.0,"vy":0.0,"life":2.0,"reflected":false}]
	x.guard=1.0;sim.tick(x,{},.01,false)
	if x.hp!=3:errors.append("xiaomo translucency incorrectly invulnerable")
	checks+=1
	var result={"passed":errors.is_empty(),"cases":checks,"errors":errors,"engine":Engine.get_version_info().string,"scope":"10 source parity vectors, seed retry, timing safety, translucency damage; no keyboard/visual claim"}
	print(JSON.stringify(result))
	var f=FileAccess.open("user://native-logic-tests.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "))
	quit(0 if errors.is_empty() else 1)
