# Notes — the-passport-page-of-a-countr-2-20261121-0318

## Top-10 study (live, 21 Nov 2026 ~11:00 WIB)

All ten leaders withhold their source (`source_withheld: true`), so this
study is titles + live scores only. No leader's method is invented here.

| # | Title | Live score |
|---|-------|-----------|
| 1 | Passport spread of the Republic of Velmora | 887,596 |
| 2 | Republic of Talmera — Passport Spread | 874,369 |
| 3 | Austere Ion | 871,719 |
| 4 | The Selmara Passport — Entry by Sea Only | 871,719 |
| 5 | Republic of Alveria — passport spread | 869,067 |
| 6 | Passport of the Republic of Skarholm | 869,067 |
| 7 | Republic of Velhara passport — Særa Ingrid Halvorsen | 869,067 |
| 8 | Republic of Skerr | 863,758 |
| 9 | Passport of the Tidal Republic of Meridia | 858,442 |
| 10 | Republic of Lumara: passport spread | 858,442 |

Pattern: a fictional republic's passport spread — a photo page plus
data/visa pages, an invented republic name, a named holder. The scored
elements the field agrees on: a complete believable spread, a portrait
with a machine-readable strip, stamps from neighbouring countries, and
one detail of paperwork that reveals the place.

## What we did differently (own recipe, world-class art)

Standing creative rule (Joni, 20 Nov 2026): do NOT copy the leaders'
visual language; find our own recipe. Differences:

- **A different country, defined by a tide, not a border.** Caelmar
  exists only at low tide; its capital Lowtown appears and disappears
  with the water. The leaders' republics are conventional land states
  (Velmora, Talmera, Alveria, Skarholm, Velhara, Skerr, Meridia,
  Lumara, Selmara).
- **A different holder story.** Mara Iversen is the Warden of the
  Sands — her job IS the territory. The portrait, the place-name and
  the country's character are one story, not a generic face beside a
  capital.
- **A different visual language.** Flat-vector engraved/document style
  (cream paper, navy ink, one red accent, DejaVu serif/sans/mono) on a
  dark desk, straight-on, instead of the field's photo-style spreads.
- **A different telling detail.** The CONDITIONS OF ISSUE box makes the
  passport valid only while the territory is above water — arrival by
  boat at low tide, departure before high water, no airport exists.
  (Leader #4's "Entry by Sea Only" is the closest idea in the field;
  ours is a tide condition, not a sea-entry condition, and it is backed
  by a tide table for the same day as the re-entry stamp.)
- **A map with a reason to exist.** "WHERE IT IS — THE NORTH SEA"
  shows the sandbank among real neighbours (Norway, Denmark, United
  Kingdom) — the same neighbours whose stamps fill the visa page.

## Verification done

- MRZ check digits recomputed independently (ICAO 9303): document,
  birth date, expiry date, personal number and composite all correct.
- All four stamps fall after the 14 MAR 2024 issue date, in travel
  order; the Schengen transit visa (02 JUN – 02 DEC 2024) covers
  exactly the Bergen/Esbjerg trip.
- Image: 1024x1024, 284,444 bytes (gate: <= 1024x1024, <= 1,048,576).
- `main.py` tested as uid 65534 on a read-only copy: output
  byte-identical to the bundled image.
- Kit check: see below (filled in after the check run).

## Kit check (21 Nov 2026 ~11:22 WIB, kit level 32)

- Result: **14 passed, 0 failed, 5 skipped, 5 checked at submission**
  (exit 0). First run failed only `license_osi` (LICENSE lacked an
  SPDX line); fixed with `SPDX-License-Identifier: MIT`, re-ran clean.
- `thinking_reproduces` 94.5% (245/259 lines authored, 0 pasted);
  `thinking_priced` passed on 1 usage record (parent session's row).
- Bundle: `~/workspace/tools/makefun/the-passport-page-of-a-countr-2-20261121-0318-transcripts.tar.gz`
  — 1,004,129 bytes, sha256
  `6a9ada112c1d45b39bf46bb65cc4333a8b5bef5e99bcd70edb737ef14c5ea145`.
- IMPORTANT for submit: this bundle was made while the builder
  (subagent) run was still in progress, so the builder's own usage rows
  are not attached yet (a subagent's rows are written only once its run
  completes) and its final turns are not in it. Before submitting,
  re-run the usage SELECT with the builder + parent agent_ids and
  re-bundle with the same flags, then re-run check. The entry was
  checked at commit `c89427ce071166e2894222338f6a40ba4ee7638b`.

## v2 rebuild (21 Nov 2026, on Joni's order "Ubah foto nya dengan foto
orang asli dan bentuk passportnya mengikuti format passport asli suatu
negara")

- Portrait: photorealistic passport photo of a fictional woman (Mara
  Iversen), generated with the image tool — NOT an illustration, NOT
  Joni, NOT a real identifiable person or celebrity. Plain light-grey
  background, front-facing, neutral expression, head-and-shoulders.
  Source: `portrait-mara-iversen.webp` (bundled in the repo);
  rendered into the data page by `render_v2.py` (Pillow, 3x
  supersample, LANCZOS to 1024x1024).
- Format: data page rebuilt to a real passport format — Indonesian
  passport / ICAO Doc 9303 TD3 data page. Photo on the left,
  personal-data fields beside it with bilingual Indonesian/English
  labels (Jenis/Type, Kode Negara/Country Code, No. Paspor/Passport
  No., Nama/Name, Kewarganegaraan/Nationality, Tempat Lahir/Place of
  Birth, Tanggal Lahir/Date of Birth, Jenis Kelamin/Sex), holder's
  signature under the photo, issue/expiry/authority below, MRZ
  (2 x 44 chars) at the bottom. The REMARKS block left the data page
  (a real biodata page has none).
- Fix found in review: "TANGGAL HABIS BERLAKU" was clipped at the
  page edge at first render (label 392px at 3x vs 342px available);
  moved the expiry column from x0+280 to x0+258, re-rendered, label
  now fits with margin.
- Unchanged: country, holder, all dates, all 4 stamps, Schengen visa,
  CONDITIONS OF ISSUE text, tide line, MRZ lines, and the whole visa
  page — the same content as v1.
- MRZ re-verified by hand (ICAO 9303, weights 7-3-1): document
  CAE004821 -> 5; birth 880612 -> 7; expiry 340314 -> 1; personal
  number (all filler) -> 0; composite over the 39 covered
  characters -> 0. All five check digits correct.
- Image: 1024x1024, 323,445 bytes (gate: <= 1024x1024, <= 1,048,576).
  `main.py` unchanged (pure stdlib, copies bundled entry.png).
  Tests: 3/3 pass (`python3 tests/test_main.py`).
- Kit check: (filled in after the check run).
- Bundle: (filled in after the re-bundle).

## Live score / rank

- Not submitted yet — this build is reported for Joni's 'Setuju' first.
- After submit: record live score and rank here.
