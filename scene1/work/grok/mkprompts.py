"""Grok test: reuse the chosen Seedance prompt per shot, swap the audio/image-2 references for
plain voice/prop descriptions (Grok image2video takes only a start frame)."""
import json, re
SRC = '/root/.claude/projects/-home-user-The-trade-code/689e96b5-ac0c-586b-a1ad-2a262654b7c1.jsonl'
SEEDS = {"01":1101,"02":1122,"03":1103,"04":1104,"05":1105,"06":1106,"07":1127,"08":1138,"09":1119,"10":1140,"11":1111,"12":1112,"13":1113,"14":1124}
# shot 02 uses seed 1122 too (shot 12 take b); disambiguate by first-frame/keyword
seen = {}
for l in open(SRC):
    try: d = json.loads(l)
    except: continue
    m = d.get('message', {})
    if not isinstance(m, dict) or not isinstance(m.get('content'), list): continue
    for c in m['content']:
        if c.get('type') == 'tool_use' and c.get('name', '').endswith('generate_video'):
            p = c['input'].get('params', {})
            seen.setdefault(p.get('seed'), []).append(p.get('prompt'))
VOICE = {"tavik": "a bright, clear young boy's voice, about eight years old",
         "vessa": "a light, high, sweet little girl's voice, about six years old, higher than the boy's",
         "dad": "a warm, mellow, friendly grown man's voice"}
def pick(sid):
    cands = seen[SEEDS[sid]]
    if SEEDS[sid] == 1122:
        key = "closed paper bag" if sid == "02" else "remember you using"
        cands = [c for c in cands if key in c]
    return cands[-1]
for sid in SEEDS:
    p = pick(sid)
    p = re.sub(r"with the voice of audio \d \((\w+)\)(: [^.]*\.)?", lambda m: "with " + VOICE[m.group(1)] + ".", p)
    p = re.sub(r",? exactly like audio \d", "", p)
    p = re.sub(r"(from|as|of) image 2[^.,]*", "", p)
    p = p.replace("exactly as image 2: ", "").replace("as image 2. ", "").replace("exactly as image 2. ", "")
    p = p.replace("Tuh-VIK", "Tuh-VEEK")
    p = p.replace('"Hey Dad! ... What\'s THAT?', '"Hey, Dad!" (a happy hello, falling at the end, a greeting not a question) ... "What\'s THAT?')
    p += "\nThe boy's name Tavique is pronounced \"tuh-VEEK\" (stress on VEEK)." if sid in ("01", "12") else ""
    open(f"prompts/{sid}.txt", "w").write(p)
    assert "audio" not in p.lower().replace("audio:", "") , (sid, re.findall(r".{40}audio.{40}", p, re.I))
    assert "image 2" not in p, sid
    print(sid, len(p))
