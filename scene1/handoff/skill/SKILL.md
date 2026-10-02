---
name: "ai-story-film"
description: "Produce a finished AI animated short film from a story (e.g. a Bible narrative): script, assets, stills, sequential video, QC and assembly. Use when Chad asks for a film, anime, CGI or story video."
---

# AI Story Film

The full method for turning a story into a finished, polished film. It was first used for "The Shepherd King" (David and Goliath, 1 Samuel 16-17, anime style, 63 shots, 10 min). The state ledger, location coverage and floor plans, the cut check, draft-then-final resolution and the automated QC were built on "The Trade" Scene 1 (Hollow Meadow, CGI, 14 shots), where Chad found continuity pops at most cuts that every earlier check had missed.

## The one rule that governs every check

Never run a check and only write a note. Every check is a loop:

1. **Check.** Look at the actual output: the image, the frames, the audio.
2. **Identify.** Name exactly what is wrong and in which shot.
3. **Fix.** Regenerate, edit or re-prompt right away.
4. **Verify.** Run the same check again on the fixed version.
5. **Move on** only when it passes.

A problem found and left in the film is a failure of this method. If a fix truly cannot be made after real attempts (3 tries with changed prompts), stop and tell Chad plainly what failed and why. Don't bury it in a list of notes at the end.

**Before spending credits on fixes, tell Chad in one short message** which shots will be regenerated and roughly what it costs. Then go ahead. He wants to know what is happening, not to be surprised by it.

**Keep the better take.** A regenerated take can be worse than the original. The verify step decides which one goes in the film, not the fact that it is newer.

**Iterate cheap, finish once (Chad's locked rule).** All images are made at 1K low quality, and regenerated as many times as it takes, since each try costs about 6 credits. Video goes straight from the approved 1K still to 480p drafts. Once a shot is right at 480p, it gets one final render at 720p. Nothing is made at 2K or 1080p unless a check shows 1K isn't holding. Quote prices from the cost tool with the exact settings (quality and resolution change the price a lot), never from memory.

## Step 0: Set the two levers

Every project has two levers. If Chad already set them in his request (for example "CGI, no narration"), use those and don't ask again. Otherwise, ask both in one AskUserQuestion call before any work.

### Lever 1: STYLE

The options are **Anime**, **CGI** or **Other**.

The chosen style becomes one fixed STYLE BLOCK.
- It opens every still prompt and every video prompt, word for word, for the whole project.
- Record it in the canon sheet.

Starting style blocks:

- **Anime:** "2D Japanese anime feature film, hand-drawn cel-shaded look, painted backgrounds, expressive eyes, clean line art."
- **CGI:** "3D CGI animated feature film, high-end stylized characters with expressive faces, soft global illumination, rich materials and textures, cinematic depth of field."
- **Other:** Chad describes the look in his own words (for example watercolor, claymation, comic-book, painterly). Write a style block from his description.

**Style test (all three options).** Before any assets:
1. Make one test image: the main character in one real location from the story.
2. Show it to Chad.
3. Adjust the style block until he approves it.

The approved test image becomes the style anchor. Include it as a reference in the character sheets.

### Lever 2: NARRATION

The options are **On** or **Off**.

- **Off:** The story is told only through dialogue, acting and sound.
- **On:** Also ask two things:
  - who the narrator is (an unseen storyteller, or a character looking back);
  - how much narration (only over establishing shots, or also bridging between scenes).

  Narration is written into the script from the start. It is never added in post.

Also ask anything else truly open about the story or length. Skip anything Chad already said.

## Step 1: Script

Cover every scene in the source text, in order.

**Dialogue**
- Highly dramatized and emotional.
- Takes its time, with dramatic pauses.
- Leaves room for characters to think, feel and struggle over their answers.
- Never rushed.
- Full sentences that name people and things, not clipped fragments.

**Acting notes.** For every shot, write what every character on screen is doing, thinking and feeling, and how they react.

**Camera.** Use advanced camera work: pans, zooms, push-ins, handheld shaky camera, drone and aerial shots, orbits, rack focus. Every camera direction in the script must be carried into that shot's video prompt word for word (for example a very slow zoom into Dad's face while he looks away and remembers). A camera note that never reaches the prompt is lost.

**No same-angle cuts.** Two shots in a row must differ in angle or size (wide to medium, front to side). Two shots from the same camera position make a jump cut, which reads as jagged (The Trade, shot 13 to 14). If the action continues in the same frame, keep it as one shot instead.

**Transitions.** Mark each shot's transition: a cut or a cross-dissolve within a scene, a fade to black between scenes, and a fade at the end.

**Sound**
- No background music.
- No ambient beds (wind, birdsong, crowd murmur).
- Only dialogue, direct on-screen sound effects, and narration if the lever is On.
- Leave at least half a second of silence across every cut between one line and the next. Plan it in the shot timing: start each shot's first line after a short beat.

**Establishing shots (required)**
- Include shots with no dialogue that just show the place, the landscape, or the action itself, to help tell the story.
- Every scene opens with one unless there is a clear reason not to.
- Use more of them at time jumps and location changes.
- Mark them in the shot list as ESTABLISHING.

**Narration (only if the lever is On)**
- Write narration lines into the script with their shot IDs.
- Establishing shots are the natural home for narration.
- Narration must not talk over character dialogue.

**Canon sheet.** Write one before any images, and use it at every check:
- **Style block and style anchor** from Step 0.
- **Height table:** each character's height as a ratio to a reference character, with plain notes.
- **Costume and props per character, per scene.**
- **Voice description per character**, plus the narrator if narration is On.
- **Name pronunciation:** how every name is said, spelled by sound ("Tavik: tuh-VIK"). Use that sound-spelling inside every video prompt where the name is spoken. In The Trade the script spelling "Tavique" came out as "Tavreak".
- **Screen geography per scene:** where each character and each key prop sits ("Vessa at the table, screen left. Dad at the counter. Tavique on Dad's right. Drawer left of the sink. Hook right of the back door."), and which coverage plate each camera angle looks at.

**State ledger (required).** For every shot, write two lines before any images:
- **START:** who is in frame and where; each person's pose (standing, kneeling, sitting, facing which way); what is in each hand; where each key prop is (in the bag, in the drawer, on the hook); camera angle and which coverage plate is behind them.
- **END:** the same list, after the shot's action.

Rules:
- The START of a shot equals the END of the shot before it. Anything that changes between them must be shown happening on screen (Dad kneels, Tavique walks to the door), either at the end of one shot or the start of the next.
- A prop appears in a hand only after the line or action that brings it out. If Vessa asks "What's that?", Dad's hands are still empty at the start of that shot and he takes it out of the bag during it. If Dad says "paintbrush", he isn't already holding the lacquer.
- A change of camera angle is fine. A change of position, pose or prop across a cut is a pop unless the ledger shows it.

Deliver the script, with the ledger, to Chad as a file before generating anything.

## Step 2: Assets

Make these first, all using the style block and the style anchor. Check each one before using it:

- **Character sheets:** each character full body, front and side.
- **Location coverage** (below).
- **Prop sheets.**

### Location coverage (required)

A single front-facing plate is not enough. Every angled shot, close-up and reverse shot then has to invent the part of the room behind the character, and each shot invents it differently. In The Trade, the flashlight close-up shone the beam onto a wall of cabinets that appears in no other shot.

For every location, before any stills, make its full coverage:

1. **The room's walls, side to side.** Either:
   - **one super-wide panorama** (about 32:9) that the camera can pan across; or
   - **three plates:** CENTER; LEFT, which repeats the left quarter of CENTER and extends the room further left; RIGHT, which repeats the right quarter of CENTER and extends further right. Make LEFT and RIGHT from CENTER as the reference, so the overlap matches.
2. **Wall views for the other walls**, named by compass direction (WEST, SOUTH...), not "reverse". Make each one only after the floor plan says what is on that wall, and describe it left to right in the prompt. A loosely described "reverse" view in The Trade put the fridge on the wrong side and a doorway into a corner where the cabinets already were.
3. **A floor plan:** a simple top-down sketch with every piece of furniture, door, window, stair and key prop (the drawer, the hook), the direction each appliance faces, which way stairs run, and the camera position for every plate and every shot. Walls no locked image shows yet are drawn dashed.

**Lock order (from The Trade):**
1. Lock the wide view (panorama or CENTER) first, with Chad.
2. Build the floor plan **only from locked images**. Read each image carefully for which wall an object is on: in The Trade the fridge stood on the west wall facing the table, and the first plan wrongly put it on the north wall.
3. Check the floor plan against the script's location notes (the script says "the drawer to the left of the sink").
4. Make every other view to match the plan. Show Chad the plan and each new view; he approves both.
5. A change to the set (the fridge and pantry cabinet swapping sides) is made on **every** plate that shows it: panorama, LEFT, RIGHT and any wall view. Then re-run the overlap check.
6. Keep a LOCKED PLATES list (plate name, direction it looks, link). Only listed plates are used as references. Old versions are marked retired.

**Every location in the series gets this:** locked views, a floor plan, and a camera spot for each shot. Keep the floor plans with the project so later episodes reuse the same rooms.

Make sure every key prop spot (the hook, the drawer, the junk box) is visible in at least one coverage plate, so close-ups of it have something to match.

Coverage checks (check, fix, verify):
- **Overlap match.** Put the shared quarter of LEFT (or RIGHT) next to the matching quarter of CENTER. Same cabinets, same window, same light. The tool (`overlap.py`) finds the same features in both: pass at 60 or more matching features and a size ratio between 0.8 and 1.25. If not, regenerate the extension with CENTER as the reference.
- **Same objects, same order.** Compare countertops and shelves item by item against the locked wide view (lemons, mixer, herb, boards, sink). Image edits often add or drop a small item. A single extra item on a plain wall can be painted out locally instead of paying for another edit.
- **Edits stay inside the edit.** Compare the edited plate with the old one: the changed area should be only where the edit was asked for.
- **Nothing added later.** Every wall, counter, table and cabinet that will ever be on screen exists in the coverage. A shot may never invent one.

**Scale lineup (required).** Make one image with all main characters standing side by side at their canon heights. Compare it to the height table. Fix it until it matches. This lineup is a reference for every later image.

Asset checks (check, fix, verify):

- **Style match.** Does it look like the style anchor?
- **Period accuracy.** For example, no red tile roofs in ancient Israel.
- **No unintended symbols.** No crosses in windows, no halos or sun glows behind someone's head, nothing that reads as a noose.
- **Age matches the brief.**

## Step 3: Voice casting and lock

Cast every speaking character with a short voice sample (about 6 seconds). If narration is On, cast the narrator too.

1. Clean each sample so only the voice remains (vocals stem; remove any hum or drone). Level it.
2. Measure and record each voice's median pitch in the canon sheet.
3. These samples are LOCKED for the whole project.
4. **A character with no sample yet** (a new adult, say): generate their first speaking shot with a written voice description, then cut 5-9 seconds of their clean speech from that clip and lock it as their sample for every later shot.

From here on:

- **Every** shot where a locked character or the narrator speaks must include that voice sample.
- Never drop the voice sample to get past a failure. That is how David's voice drifted in The Shepherd King (shot 14.3 was made without it).
- If a shot keeps failing with the sample attached, change the wording, not the voice.
- Seedance takes at most 15 seconds of voice audio per shot in total. For two-speaker shots, trim the longer sample so both fit.

## Step 4: Storyboard stills

**Stills are a chain, not a set.** Even when Chad asks for all the stills before any video, each still is built from the one before it:

- Shot 1's still comes from the coverage plate for its angle, the character sheets and the scale lineup.
- Every later still is made from [the previous still + the coverage plate for this shot's angle + character sheets + scale lineup], and must match the previous shot's END state from the ledger, seen from the new angle.
- In The Trade every still was made separately from one master wide shot. Each shot started from a fresh pose, and 11 of 13 cuts popped.

Make establishing-shot stills the same way, as landscape or action only.

Check every still (check, fix, verify):

- **Style.** Matches the style anchor.
- **Background matches coverage.** The part of the room behind the characters matches the coverage plate for this angle. No invented walls, cabinets, tables or counters.
- **Ledger match.** People, poses, hands and props match this shot's START state. Nobody is holding something the script hasn't brought out yet.
- **Pair check.** Put it next to the previous still. Same people, poses, props and set, from a different angle or size (never the same angle).
- **Continuity.** Same costume, hair, props and lighting as the canon sheet.
- **Scale.** Compare character heights to the height table.
- **Unintended readings.** Ask what someone seeing this frame with no context would think it says.
- **Count checks.** Exactly one lamp, one servant boy, the right number of brothers.
- **Start state.** If the action changes something (a light switches on, a door opens), the still shows the BEFORE state.

Show Chad a contact sheet of all stills in order, in pairs.

### Stills at 1K low (Chad's locked rule)

1. **Make every image at 1K, low quality**: storyboard stills, opening stills, location plates, character sheets, the scale lineup. GPT Image 2.5 Sunburst costs 7 credits list (about 6 after the discount) against 152 for 2K high.
2. **Regenerate freely.** A still with an error is regenerated, not fixed with an expensive edit. Run every still check on each try.
3. **The approved 1K still goes straight into the video** as the opening frame. There is no 2K remake step. At 16:9 a 1K image is 1792 x 1008, bigger than the 720p final video.
4. **Only if a check fails because of detail** (a face, hand or small prop that 1K low can't render cleanly after several tries) make that one image at 1K medium (32 list) or 2K. Tell Chad first.

**Tested on The Trade, October 2026:**
- The locked wide kitchen remade at 1K low came back almost identical to the 2K high original: every cabinet, countertop item, the door, hook and pantry in place; leaves and worn paint only slightly softer.
- A three-character still at 1K low kept Dad, Tavique and Vessa on-model (faces, hair, clothes, bows, shoes) and kept the height difference. Dad's beard came out slightly smoother and the paper bag lost its handles.
- It also staged Vessa impossibly: her upper body on the far side of the table and her legs on a chair on the near side. That is a staging error, not a resolution error, and it was easy to see at 1K low. The still checks catch it; regenerate.

## Step 5: Video, built in sequence

Generate in cut order, scene by scene. Never in parallel across a scene: each shot needs the one before it.

1. Every video prompt opens with the style block, then: "exactly matching the art style, character designs, costumes and location of image 1, which is the opening frame of this shot."
2. The first shot of a scene starts from its checked storyboard still.
3. Every following shot:
   - take the last frame of the previous clip;
   - make a new opening still from [that last frame + the storyboard still + the coverage plate + character sheets + scale lineup], with written continuity and scale notes from the ledger;
   - check that still (the pair check against the last frame, and background against coverage);
   - generate the clip from it.
4. Every speaking shot carries the locked voice samples. The prompt says who speaks with which voice.
5. Every prompt states: dialogue exactly as written; names spelled by sound; only dialogue and direct sound effects; no music, score, humming, choir, drums or ambient bed; no subtitles.
6. **Write the acting as a timeline:** "0-0.6s beat, no one speaks. 0.6-4s Vessa leans in and says... 4-5s Dad smiles... 5-13s Dad reaches into the bag, lifts out the flashlight and says...". Give listeners a reaction in every beat. Put pauses in the lines with "..." and stress one word in CAPS. Size the clip length to the lines.
7. **End the shot on the next shot's START.** If the next shot has Dad standing, this shot ends with him getting up.
8. **Camera words the model takes too far.** "Slow push-in" can become a push-in plus an invented hard cut to a new angle. When the shot must stay one angle, write "CAMERA: LOCKED OFF. No zoom, no push-in, no pan, no cut to another angle." For a scripted zoom, say how slow and onto what ("a very slow, continuous zoom toward Dad's face over the whole shot, no cut"). For a pan, include the matching coverage plates as references.
9. **Stability lines** for anything that drifted before: "Dad's body, build and clothes stay exactly as in image 1 in every frame. The cabinets stay exactly as in image 1."
10. Establishing shots:
   - Narration Off: "No dialogue" plus only the direct sound effects of the action.
   - Narration On: add the narration as an unseen voice using the narrator's locked sample, and state that no one on screen speaks.

**When the audio moderation rejects a clip as "copyright":** reword the line slightly, keep its meaning, and describe the sound as "a dry, plain dialogue recording." Keep the voice sample attached.

**Upstream errors** ("CreateAsset failed", "EOF") are server hiccups. Resubmit the same request unchanged.

### Draft first, final second (resolution)

Get each shot right cheaply, then pay for quality once.

1. **Draft at 480p.** Generate every shot at 480p first. Run the full QC (Step 6) and the cut check on the drafts. Fix and re-draft at 480p until the scene passes and Chad approves it.
2. **Record what made the approved draft:** the exact prompt, the opening still, the references, the voice samples, the duration and the seed. Seedance picks a random seed when it is left at -1, so set a seed on every draft and keep it in the shot list.
3. **One final at 720p.** Once a shot is right at 480p, regenerate it once at 720p with the same 1K opening still, prompt, references, voices, duration and seed. (Chad's locked rule.)
4. **QC the finals again, all of it.** A final render is a new take. Not yet validated: whether the same seed gives the same acting, timing and lip-sync at a higher resolution. Expect some finals to come out different. Compare each final to its approved draft (the cut pair, the timing of lines, the action); if it is worse, retry it at 720p.
5. **Upscale the approved 720p finals with Chad's Topaz** to 1080p or 4K for delivery. Never upscale the 480p drafts as finals.
6. Tell Chad the final-pass cost before starting it (see the price table under Validated tools).

**Why 720p, not 480p, as the upscale source (tested on The Trade frames, October 2026):** an AI upscale from 480p held up in close-ups, but fine texture (Dad's beard, the worn cabinet paint) came out smooth and plastic, and small faces in wide shots came out soft and guessed. From 720p the texture survived. 720p has about 2.25 times the pixels of 480p, and an upscaler can only guess at detail that isn't there. Chad's Topaz (perpetual v3.2.9) is a straight resolution increase that adds no detail, so the source resolution matters even more than in that test. 720p finals cost 720 credits per 10 s after the discount, against 1,800 at native 1080p.

The first time this runs, test it on one shot (draft and final with the same seed, side by side) and record here whether the take carries over.

## Step 6: Per-clip QC (check, fix, verify, then move on)

Run the QC checker (`film_qc.py` + a `shots.py` shot list, built on The Trade) on every clip, then the cut check, then the eye pass. A clip moves on only when all three pass.

### 6a. What the checker does on every frame

- **Black frames** and **frozen picture** (no change for 1.5 s or more).
- **Hidden cut:** the picture's meaning jumps from one frame to the next, inside what should be one continuous shot.
- **Glitch / pop:** a sudden jump in structure far below the shot's own local norm while the meaning stays. Compare to a rolling median, never to one fixed number.
- **Drift:** each frame compared to the approved still. A drop of more than 0.12 below the shot's own first second means a character or the set changed.
- **Presence and screen order:** each main character tracked by costume colour.

### 6b. What the checker does on the audio

- **Words:** transcript vs script, letter by letter. More than 10% different fails.
- **Names:** every spoken name compared to the canon pronunciation. Never blur names together in the word check. A name that is close but wrong ("Tavreak", "Taviki") fails.
- **Voice (speaker ID):** each line compared to that character's other lines in the episode. Below 0.80, or closer to another character, fails. Do not fail a line on pitch alone: children's pitch swings 20-35% with emotion.
- **Music / ambience:** a held steady note (0.6 s or more) between lines is music. Loud unvoiced noise for 1.5 s or more is an ambient bed. A chuckle or breath at the character's own pitch is not.
- **Peaks** hitting 0 dBFS.

### 6c. The cut check (required, every cut)

This is the check that was missing. Every earlier check looked at one shot at a time, so it could not see a pop between shots.

1. For every cut, put the last frame of shot N beside the first frame of shot N+1 (the checker makes this sheet).
2. Compare the pair against the ledger, item by item: same people in the scene (even if off-frame now), same pose, same thing in each hand, props where they were, same furniture, background matching the coverage, expressions continuing.
3. Any change not shown on screen is a fail: kneeling to standing, a character turned the other way, someone vanishing from beside another, a table moving, new cabinets, the drawer changing.
4. **Jump cut:** the two frames are from the same camera angle and size (image-similarity 0.88 or higher across the cut). Fail; change the angle or merge the shots.
5. **Sound across the cut:** less than 0.5 s of silence between the last line of shot N and the first line of shot N+1 fails.
6. The checker's numbers (a character vanishing or appearing, a big position jump, a size jump) say which cuts to look at first. They cannot decide alone, because they can't tell a new camera angle from a pop. The pair review decides.
7. Fix by remaking the next shot's opening still from the previous shot's last frame, then regenerating the clip. Re-run the pair check.

### 6d. The eye pass

Look at every clip at 2 frames a second, and the cut sheet. The checker does not catch these:

- **Lip-sync:** does only the speaking character's mouth move?
- **Action matches the line:** is the prop introduced when the line introduces it? Does the action the line describes actually happen (Dad reaches into the bag)?
- **Blocking:** does a character wander when they should stay put?
- **Camera:** is the scripted move there (the slow zoom), and nothing else?
- **Background:** in close-ups and angled shots, does the room behind the character match the coverage plates? Is whatever a character points at, looks at or lights up something that exists in the coverage?
- **Performance:** does the acting read as intended?

### 6e. Pass rule

A clip passes when the checker shows no flags, words, names and speaker ID pass, no bed, the cut pair on both sides passes, and the eye pass is clean. When you regenerate, run everything again on the new take and keep whichever take passes.

## Step 7: Whole-film checks before assembly

These are also check, fix, verify.

- **Cut sheet:** every cut in the film, last frame beside first frame, reviewed against the ledger.
- **Voice across the film:** a table of every speaking line with its speaker-ID score and every spoken name.
- **Scale across the film:** a contact sheet of every shot where size matters, side by side.
- **Continuity and style:** a contact sheet of every shot in order.
- **Before/after sheet:** for every shot that was fixed, frames from the old and new take side by side. Show Chad.

## Step 8: Assembly and delivery

1. **Assemble.**
   - Title card.
   - Transitions as scripted: cuts, dissolves, fade to black between scenes and at the end.
   - Per-clip audio choice (original, voice-only, or muted).
   - Level each clip's loudness, then join the clips with a join that re-encodes the sound as one track. A straight copy-join played silent on Chad's phone.
2. **Verify the finished file.**
   - Picture and sound stay in sync all the way through.
   - Pull frames from across the film and look at them.
   - Measure the overall loudness.
   - Encode for phones: H.264 Main profile, AAC stereo, "faststart" on.
3. **Deliver.**
   - Chat attachments max out at 30 MB. Send a small full-length version plus the high-quality film in parts under 30 MB.
   - Also send an audio-only MP3.
   - Also upload one full-quality file to OpenArt (limit 200 MB). Give Chad the link.
   - If his computer is linked, save the full file into his folder.
4. **Report in plain language.**
   - What's in the film.
   - Which style and narration settings were used.
   - Anything that could not be fixed, and why.
   - Credits used.

## Validated tools (OpenArt)

- **Stills:** GPT Image 2.5 Sunburst, image-to-image, **1K, low quality** (Chad's locked rule, see Step 4). Earlier projects used Seedream 5 Pro at 2K (anime) and GPT Image 2.5 Sunburst at 2K high (CGI).
- **Precise edits:** Nano Banana Pro, or GPT Image 2.5 Sunburst with "change ONE thing only".
- **GPT Image 2.5 Sunburst prices** (image-to-image, list before the 10% MCP discount, checked October 2026): 1K low 7, 1K medium 32, 1K high 117, 2K medium 42, 2K high 152. In The Trade, plate edits were run at 2K high and quoted to Chad as 42 each; the real cost was about 137 each. Check the exact settings with the cost tool before quoting.
- **Coverage extensions:** GPT Image 2.5 Sunburst image-to-image with the CENTER plate as reference made LEFT and RIGHT plates that passed the overlap check (630 and 207 matching features). A one-shot 32:9 panorama came out reframed (size ratio 0.72) but was still usable as the locked wide view once Chad approved it. Set changes (swapping two objects) across all plates worked in one edit each; wall views made from a written left-to-right description plus the locked plates as references worked on the first try.
- **Video:** Seedance 2.0, element-to-video, with generated audio. Drafts at 480p, finals at 720p, then Topaz to 1080p or 4K (see "Draft first, final second").
  - Resolutions: 480p, 720p, 1080p and 4K. 4K is the highest.
  - Price per 10-second shot with audio (list, before the 10% MCP discount, checked October 2026): 480p 350, 720p 800, 1080p 2,000, 4K 4,000 credits. Fast mode at 480p is 300. Always re-check with the cost tool before quoting.
  - References: the opening still, plus the voice samples tagged as voice references.
  - Only about 8 videos run at once.
  - Standard Seedance 2.0 only: no Mini, and no 2.5.
  - Not Veo 3.1 for dialogue: on OpenArt it takes no voice sample and clips max out at 8 seconds.
- **QC tools (run locally in the session):** ffmpeg, OpenCV, CLIP image similarity (open_clip ViT-B-32), faster-whisper for transcripts, Resemblyzer for speaker ID, Parselmouth for pitch and voicing. A 2.5-minute scene takes about 12 minutes to check on a small machine.
- **Upscaling:** Chad's Topaz, run locally, on the approved 720p finals only.

The anime style is validated end to end (The Shepherd King). CGI is validated through video and QC for one scene (The Trade, Scene 1). Other has not been run through this full method yet.

## Lessons from The Shepherd King

- "The sun behind his head" in a prompt produced a halo, and the character read as Jesus. Don't light a character with the sun behind their head.
- A still that says "one lamp" can still come out with two. Count, and fix with a direct edit.
- Goliath's size drifted in the late battle shots. The scale lineup and scale checks exist for this.
- David's voice went higher in three shots. The voice check exists for this, and so does the rule never to drop the voice sample.
- Quotes from the Bible that sound famous can trip the audio moderation. Reword slightly rather than dropping the voice.
- Notes were written about problems that were then left in the film. The check, fix, verify loop exists for this.

## Lessons from The Trade (Scene 1)

- Every still was made separately from one master wide shot instead of as a chain. Chad then found pops at 11 of 13 cuts: Dad kneeling and standing with no move between, Tavique vanishing and turning, the table moving, new cabinets appearing, the drawer changing, Vessa's chair jumping. No check caught them, because every check looked at one shot at a time. The state ledger, the chained stills and the cut check exist for this.
- Only one front-facing kitchen plate existed. Close-ups and angled shots invented the rest of the room, and the flashlight beam landed on a wall of cabinets seen nowhere else. Location coverage exists for this.
- Shots 13 and 14 were from the same wide angle with 0.38 s between lines: a jagged jump cut. The same-angle rule and the half-second rule exist for this.
- Stills showed props already in hand before the line brought them out (Dad holding the flashlight as Vessa asks "What's that?"; holding the lacquer while he says "paint"; never reaching into the bag for the screws). The ledger's prop rule and the eye pass's "action matches the line" item exist for this.
- The word check blurred all "Tav-" names together, so "Tavreak" passed. Names are now checked on their own, against a sound-spelling.
- A scripted slow zoom on Dad's face during his memories never made it into the prompt. Camera notes must be carried into the prompt.
- A "slow push-in" became a push-in plus a hard cut to a new angle. Locked-off camera wording fixed it.
- Dad's body reshaped mid-shot. The drift check caught it; a stability line fixed it.
- The first automated checker flagged every camera move as a glitch, every chuckle as music, and four children's lines as the wrong voice. All were false alarms. Tune a new check against the eye pass before trusting it.
- Two regenerations weren't needed, and one made the shot worse (it invented a line). Verify every new take and keep the better one.
- A straight copy-join of clips played silent on Chad's phone. Re-encode the sound when joining.
- The first floor plan was drawn before the views were locked, and two plates disagreed about which wall held a doorway. Building the plan only from locked images, then making the other wall views to match it, fixed it.
- The kitchen drawer was placed right of the sink for a whole shot list, but the script says left. Check the floor plan against the script's location notes.