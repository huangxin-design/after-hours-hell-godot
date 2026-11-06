extends RefCounted

# Engine-neutral metre-space rules ported from the tested logic.mjs.
var data = {}
var nav = {}
var blocked = {}
var obstacles = []
var events = []
var templates = [
	{"id":"alternating","offsets":[0.0,1.8]},
	{"id":"reverse_stagger","offsets":[1.8,0.0]}
]

func _init():
	data = JSON.parse_string(FileAccess.get_file_as_string("res://data/migration.json"))
	nav = data.navigation
	for cell in nav.blocked: blocked[int(cell)] = true

func create_state(checkpoint=false, evidence=false, run_seed=0, hero="guozai"):
	var s = data.checkpoint_retry_state.duplicate(true) if checkpoint else data.initial_state.duplicate(true)
	s.evidence = evidence
	s.checkpoint = checkpoint
	s.hero = hero
	s.seed = int(run_seed)
	s.template_index = posmod(int(run_seed),templates.size())
	s.template_id = templates[s.template_index].id
	s.decoy = null
	s.decoys_hit = 0
	s.skill_uses = 0
	s.dodges = 0
	return s

func point(name): return Vector2(data.points[name][0],data.points[name][1])
func distance(s,p): return Vector2(s.x,s.y).distance_to(p)

func floor_height(x,y):
	for z in data.zones:
		var r=z.rect
		if x>=r[0] and x<=r[0]+r[2] and y>=r[1] and y<=r[1]+r[3]:
			if z.ramp_axis == null: return z.height_start
			var t=(x-r[0])/r[2] if z.ramp_axis=="x" else (y-r[1])/r[3]
			return lerp(float(z.height_start),float(z.height_end),t)
	return null

func can_stand(x,y,cleared=false,use_navigation=true):
	if not cleared and x<22 and x>10 and y>19.4: return false
	for i in range(12):
		var a=i*PI/6
		if floor_height(x+cos(a)*.8,y+sin(a)*.8)==null: return false
	if use_navigation:
		var ix=int(floor((x-nav.origin[0])/nav.step+.5))
		var iy=int(floor((y-nav.origin[1])/nav.step+.5))
		if blocked.has(iy*int(nav.width)+ix): return false
		for b in obstacles:
			if x>b[0]-.8 and x<b[2]+.8 and y>b[1]-.8 and y<b[3]+.8: return false
	return true

func emit_event(kind,source_id="",cause=""):
	events.append({"kind":kind,"source_id":str(source_id),"cause":cause})

func hurt(s,cause):
	if s.invulnerable>0: return
	s.hp-=1; s.hits+=1; s.invulnerable=1.3
	s.message="受伤！观察预警，及时移出危险区。"
	emit_event("player_hurt","",cause)
	if s.hp<=0:
		s.phase="lost";s.message="这锅没接住。按 Enter 从检查点重试。"
		emit_event("fail")

func damage_boss(s,cause):
	s.bossHP=max(0,s.bossHP-1)
	emit_event("boss_damage","",cause)
	if s.bossHP==0:
		s.cleared=true;s.bossMode="done";s.projectiles=[]
		s.message="甩锅机已停机，长桥开放。前往下班闸。"
		emit_event("boss_stop")

func tick(s,input,dt,use_navigation=true):
	events=[]
	if s.phase!="playing": return s
	dt=clamp(dt,0.0,.05)
	s.time+=dt;s.invulnerable=max(0.0,s.invulnerable-dt)
	s.guard=max(0.0,s.guard-dt);s.guardCooldown=max(0.0,s.guardCooldown-dt)
	if s.get("decoy")!=null:
		s.decoy.life-=dt
		if s.decoy.life<=0:s.decoy=null
	if input.get("guard",false) and s.guardCooldown==0:
		s.skill_uses=s.get("skill_uses",0)+1
		if s.get("hero","guozai")=="xiaomo":
			s.decoy={"x":s.x,"y":s.y,"life":3.0}
			s.guard=3.0;s.guardCooldown=6.0
			emit_event("decoy_deploy")
		else:
			s.guard=.65;s.guardCooldown=1.15;emit_event("guard_activate")
	var movement=Vector2(input.get("x",0.0),input.get("y",0.0))
	var speed=2.6 if s.guard>0 and s.get("hero","guozai")=="guozai" else 4.2
	if movement.length()>0:
		movement/=max(1.0,movement.length());movement*=dt*speed
		if can_stand(s.x+movement.x,s.y,s.cleared,use_navigation):s.x+=movement.x
		if can_stand(s.x,s.y+movement.y,s.cleared,use_navigation):s.y+=movement.y
	var p=Vector2(s.x,s.y)
	if s.evidence and p.distance_to(point("checkpoint"))<1.8:s.checkpoint=true
	var offsets=templates[s.get("template_index",0)].offsets
	for i in range(2):
		var h=s.stamps[i];var t=fposmod(s.time+offsets[i],4.0)
		var prior=h.phase
		h.phase="safe" if t<2 else "warning" if t<3 else "impact" if t<3.38 else "rising"
		h.progress=t
		var attack_id=str(i)+":"+str(int(floor((s.time+offsets[i])/4.0)))
		if h.phase!=prior and h.phase=="warning":emit_event("stamp_warning",attack_id)
		if h.phase!=prior and h.phase=="impact":emit_event("stamp_drop",attack_id)
		if h.phase=="impact" and p.distance_to(Vector2(h.x,h.y))<1.12:hurt(s,"stamp")
	if s.phase!="playing":return s
	if input.get("interact",false):
		if not s.evidence and p.distance_to(point("evidence"))<2:
			s.evidence=true;s.checkpoint=true;s.message="责任单已取得，检查点已激活。沿坡道前往审判台。";emit_event("evidence_take")
		elif s.evidence and not s.submitted and p.distance_to(point("submit"))<2:
			s.submitted=true;s.bossMode="warning";s.bossTimer=1.6
			s.target=[s.decoy.x,s.decoy.y] if s.get("decoy")!=null else [s.x,s.y]
			s.message="防护解除！观察锁定位置，避开或反弹飞锅。";emit_event("evidence_submit");emit_event("boss_warning",s.nextId)
		elif s.submitted and not s.cleared and s.bossMode=="open" and p.distance_to(point("overload"))<2:
			s.message="按下成功！";emit_event("overload_success");damage_boss(s,"overload")
			if not s.cleared:s.bossMode="rest";s.bossTimer=1.4
		elif s.cleared and p.distance_to(point("exit"))<2:
			s.phase="won";s.reward=true;s.message="本关通关！实际打印奖励尚未开放。";emit_event("level_clear")
	if s.submitted and not s.cleared:
		s.bossTimer-=dt
		if s.bossTimer<=0:
			if s.bossMode=="warning":
				var v=(Vector2(s.target[0],s.target[1])-point("boss")).normalized()*6
				s.projectiles.append({"id":s.nextId,"x":point("boss").x,"y":point("boss").y,"vx":v.x,"vy":v.y,"life":5.0,"reflected":false})
				s.nextId+=1;s.bossMode="open";s.bossTimer=4;s.message="停机按钮亮了！靠近按 E。";emit_event("boss_throw",s.nextId-1)
			else:
				s.bossMode="warning";s.bossTimer=1.6
				s.target=[s.decoy.x,s.decoy.y] if s.get("decoy")!=null else [s.x,s.y]
				emit_event("boss_warning",s.nextId)
	for b in s.projectiles:
		b.x+=b.vx*dt;b.y+=b.vy*dt;b.life-=dt
		if not b.reflected and s.get("decoy")!=null and Vector2(b.x,b.y).distance_to(Vector2(s.decoy.x,s.decoy.y))<.6:
			s.decoy=null;s.decoys_hit+=1;b.life=0;emit_event("decoy_hit",b.id)
		elif not b.reflected and p.distance_to(Vector2(b.x,b.y))<.85:
			if s.guard>0 and s.get("hero","guozai")=="guozai":
				b.reflected=true;s.reflections+=1
				var v=(point("boss")-Vector2(b.x,b.y)).normalized()*9
				b.vx=v.x;b.vy=v.y;s.message="反弹！停机按钮会多亮一会。";s.bossMode="open";s.bossTimer=5;emit_event("guard_reflect",b.id)
			else:hurt(s,"projectile");b.life=0
		if b.reflected and not s.cleared and point("boss").distance_to(Vector2(b.x,b.y))<1.1:
			b.life=0;s.message="反弹命中！甩锅机受到伤害。";damage_boss(s,"reflection")
			if not s.cleared:s.bossMode="open";s.bossTimer=5
	s.projectiles=s.projectiles.filter(func(b):return b.life>0)
	return s

func objective(s):
	if s.phase=="won":return "已下班 · 样片通关"
	if not s.evidence:return "01 取证 · 穿过落印桥，靠近档案台按 E"
	if not s.submitted:return "02 提交 · 沿坡道到审判台，按 E 提交"
	if not s.cleared:return "03 停机 · 躲过攻击，按钮亮起时靠近按 E"
	return "04 下班 · 通过长桥，抵达出口按 E"
