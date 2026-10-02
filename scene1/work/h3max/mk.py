"""H3 Max test: the chosen Seedance prompts for shots 1-4 as-is (same voice/prop references),
with shot 1's greeting note and the name written tuh-VEEK."""
exec(open('../grok/mkprompts.py').read().split('VOICE =')[0])
for sid in ["01","02","03","04"]:
    c = seen[SEEDS[sid]]
    if sid == "02": c = [x for x in c if "closed paper bag" in x]
    p = c[-1].replace("Tuh-VIK", "Tuh-VEEK")
    p = p.replace('"Hey Dad! ... What\'s THAT?', '"Hey, Dad!" (a happy hello, falling at the end, a greeting not a question) ... "What\'s THAT?')
    open(f"prompts/{sid}.txt","w").write(p); print(sid, len(p))
