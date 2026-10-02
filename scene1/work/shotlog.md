# The Trade — Scene 1 rebuild log (480p drafts)

STYLE: 3D CGI animated feature film, high-end stylized characters with expressive faces, soft global illumination, rich materials and textures, cinematic depth of field.
Voices: TAV LOdVRizOsBzWjjM01gq3 (6.0s) · VES Y8hUGTTJCylkzhiq4faI (5.0s) · DAD y5QgLykITWN5b0bZyfCy (9.2s) / DAD_S iQOXR3ZpGoZz6G106WMu (8.5s, two-speaker shots)
LEFT plate (hand-fixed) uploaded: hZhY2I2qEiRmI6klCgfu

| # | still | seed | dur | clip | QC | notes |
|---|---|---|---|---|---|---|
| 01 | S01a FAIL (Vessa body behind table, legs on near chair) | | | | | |
| 01 | S01b PASS (…1790905498320_21837cf4.png) | 1101 | 15 | 01_a …1790905802610_79d9d488.mp4 | PASS: name tavik, words ok (recognizer misses only), voice TAV .84 DAD .98, no bed, locked cam, no pops | |
| 02 | S02a PASS (…1790906081509_4df0bbca.png) | 1102 | 10 | 02_a FAIL: clip opened off-still (Dad's hand off bag = pop) | | |
| 02 | same | 1112 | 10 | 02_b FAIL eye pass: Vessa turns to camera to deliver line | | |
| 02 | same | 1122 | 10 | 02_c …1790907019025_9c677a25.mp4 | PASS: cut pair ok, Vessa faces Dad, ends hands at bag; voice VES .852 (TAV .849 — kids' refs sit close), DAD .91. Words: offline recognizer can't read Vessa reliably — unverified. Silence 01→02 = 0.50 s (limit). | |
| 03 | S03a FAIL (back door shut) → S03b PASS (…1790907298798_c0282f5b.png) | 1103 | 12 | 03_a …1790907595603_5c1a5334.mp4 | PASS: props on their lines, voice DAD .83 TAV .81, recognizer "f-word" hits are unvoiced rattle/rustle (checked: 0% voiced), cut 02→03 0.70 s | |
| 04 | S04a PASS (…1790907775492_f12dfec5.png) | 1104 | 13 | 04_a …1790908105526_56d1c7c3.mp4 | PASS: brush to corner, set down, lacquer out on its word; DAD .93; words ok; cut 03→04 2.36 s | |
| 05 | S05a PASS (…1790908233954_42546db6.png) | 1105 | 14 | 05_a …1790908607591_875f051a.mp4 | PASS: can down, Vessa points facing Dad, red package only after her line; DAD .95 VES .86; Dad words exact; cut 04→05 1.06 s | |
| 06 | S06a PASS (…1790908833075_fffb7d94.png) | 1106 | 7 | 06_a …1790909037753_e459cf7b.mp4 | PASS: TAV .88, words ok ("oh wait" = recognizer on "But wait"), locked CU, bg stable; speech ends 6.85 s | |
| 07 | S07a | 1107 | 12 | 07_a FAIL: camera panned left; Dad opened an invented drawer by the fridge (real drawer hidden behind Vessa's head) | | |
| 07 | S07b re-framed PASS (…1790909701366_f69a640e.png) | 1117 | 12 | 07_b …1790910236520_9ec58274.mp4 | PASS w/ NOTE: right drawer (cup pull, left of sink), words exact, DAD .90, cut 06→07 0.74 s. NOTE: slow motivated pan following Dad despite LOCKED OFF (both takes) — flagged for Chad | |
| 08 | S08a FAIL (door shut, bag/props gone) → S08b PASS (…1790910548467_3815598c.png) | 1108 | 15 | 08_a …1790911254414_7b82e5e0.mp4 | PASS w/ NOTE: flashlight out of drawer, drawer closed, walk, kneel on screen; DAD .90; words ok. NOTE: model added a hard cut at 10.5 s (wide → medium two-shot, looking N). Cut is continuity-clean (kneeling, flashlight in hand) → treated as an intended edit 8a/8b; flagged for Chad. | |
| 09 | S09a FAIL (door shut) → S09b PASS (…1790911502475_0929eda9.png) | 1109 | 15 | 09_a …1790911816708_fc2abc48.mp4 | HOLD: picture passes (handover, thumb on switch, TAV .90 DAD .91) but "old and faithful" scores same as "old unfaithful" (0.648 vs 0.658) + 08→09 gap 0.48 s → retake with stressed AND | |
| 09 | S09b | 1119 | 15 | 09_b …1790912289830_e42dadf0.mp4 | PASS (chosen): "old ... AND faithful" now separated (old 5.16 s, and 6.47 s); "click it" > "quickly"; TAV .87 DAD .92; cut 08→09 1.37 s | |
| 10 | S10a PASS (…1790912520470_7bacaa20.png) | 1110 | 6 | 10_a …1790912804945_fdc935a6.mp4 | PASS w/ minor note: click 1.4 s then line; "it works it's bright" best phrase score; TAV .81; ends smiling. Beam glow lands on the wall just above the leaning doors (existing set). | |
| 11 | S11a PASS (…1790912948489_755d3650.png) | 1111 | 15 | 11_a …1790913238123_d487bf28.mp4 | PASS: scripted very slow continuous push-in to tight on Dad, eyes drift + return; all memory lines; DAD .93; cut 10→11 0.96 s. Speech runs to 14.98 s → next shot needs ≥0.6 s opening beat | |
| 12 | S12a PASS (…1790913490695_57ae7ac8.png) | 1112 | 13 | 12_a …1790913769537_d243e1fa.mp4 | FAIL: Vessa starts at 0.18 s (cut gap 0.24 s); Vessa voice closer to TAV (f0 319 vs sample 391). Name OK. | |
| 12 | same | 1122 | 13 | 12_b …1790914182633_d518f14c.mp4 | FAIL: name = "Tavreak/Taveek". Silence 1.21 s ok, Vessa f0 373 ok (VES .828 > TAV .814). Picture ok. | |
| 12 | same | 1132 | 13 | 12_c …1790914721554_ac30fcf0.mp4 | FAIL: hidden cut 7.71 s; Vessa voice closer to TAV | |
| 12 | — | — | 13 | 12_d = 12_b picture + audio with Dad's name word (0.57 s) spliced from 12_a | CHOSEN, FLAG FOR CHAD: 3 tries used. Name check passes on name-centred windows, fails on two wide windows (checker ambiguity). Listen at 8.8 s. | |
| 13 | S13a PASS (…1790914460634_92fb6bf6.png) | 1113 | 14 | 13_a …1790914923649_8ae432f1.mp4 | PASS: Dad lines ok; Tav "okay thanks dad" / "i'll keep it on the hook" best phrase scores; DAD .93 TAV .92; Tav exits, Dad alone; cut 12→13 0.91 s. Minor: flashlight beam flickers back on once after the click-off. | |
| 14 | S14a PASS (…1790915029859_1b82b38c.png) | 1114 | 11 | rendering | | |
| 14 | S14a | 1114 | 11 | 14_a …1790915287639_63f560f9.mp4 | picture PASS; Tav "On the hook" whispered, unclear words; voice .83 vs his in-episode lines | |
| 14 | S14a | 1124 | 11 | 14_b …1790915740613_ce7e570b.mp4 | CHOSEN: words clear ("...not in a pile ... on the hook"), DAD .91, hangs + settles + hold; Tav voice .79 vs in-episode (Ves .73) — FLAG, just under 0.80 | |
