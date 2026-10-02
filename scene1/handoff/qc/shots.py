# Scene 1 shot manifest: expected dialogue (speaker, text) and still used
S="https://cdn.openart.ai/openart-ai/production/2026-09/create-image/sKzm6Mb8mw10m819HD7k/gpt-image-2.5-sunburst-edit-1_"
SHOTS=[
 ("01","V01",[("TAV","Hey Dad! What's that? You went to the store?"),("DAD","Hey Tavique! What's what? Oh, this? Yeah. I needed to pick up some items to fix these old cabinets in the kitchen.")],"S01"),
 ("02","V02",[("VES","The ones that are all sanded and dusty?"),("DAD","Yep! Those ones. Let me show you what's in the bag.")],"S02"),
 ("03","V03",[("DAD","Screws. For the hinges. A paintbrush."),("TAV","That's a little brush.")],"S03"),
 ("04","V04",[("DAD","It's for the corners so the paint can go all the way to the edges. And, lacquer. So the wood doesn't stay rough.")],"S04"),
 ("05","V05",[("VES","There's something else in there. What's that?"),("DAD","This? This is a brand-new flashlight. Still in the sleeve. For under the sink and the shed.")],"S05"),
 ("06","V06",[("TAV","But wait... How come we need two flashlights?")],"S06"),
 ("07","V07",[("DAD","We don't. I'm putting the new one in the drawer. Which means this old one... wait, let me get it.")],"S07"),
 ("08","V08",[("DAD","This scuffed one right here. The one that's been in this drawer since before you could reach the counter. That means this one belongs to you now.")],"S08"),
 ("09","V09",[("TAV","You're giving me the old scratched one?"),("DAD","I'm giving you the old and faithful one. The one that has proven itself. Go ahead. Click it.")],"S09"),
 ("10","V10b",[("TAV","It works. It's bright.")],"S10b"),
 ("11","V11",[("DAD","It's bright, and it's reliable. I used it in the shed. I used it in that storm when the power went out. I used it under the sink when the pipe leaked. It never quits.")],"S11"),
 ("12","V12",[("VES","That's the good one. I remember you using it."),("DAD","That's why I want you to have it, Tavique. Not the new one. This one.")],"S12"),
 ("13","V13",[("DAD","It's special because it already proved it. You take care of a light like that."),("TAV","Okay. Thanks, Dad. I'll keep it on the hook.")],"S13b"),
 ("14","V14",[("DAD","Good idea. Keep it on the hook. Not in a pile."),("TAV","On the hook.")],"S14"),
]
# who is expected visible (by costume color) in each shot, and expected screen order left->right
VISIBLE={"01":"VDT","02":"VD","03":"VDT","04":"DT","05":"VDT","06":"T","07":"VDT","08":"VDT","09":"DT","10":"T","11":"DT","12":"VDT","13":"VDT","14":"VDT"}
