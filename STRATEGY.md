# Strategy — The Passport Page of a Country That Isn't There

## The brief, as the judge states it

The judge is a passport-control officer with a typographer's eye. It
compares two invented passport spreads and picks the one that most
convincingly reads as a document from a real country, weighing in order:

1. It must be an invented passport spread at all.
2. Typography and layout that hold together as one coherent document —
   consistent type sizes, rules, margins.
3. Stamps, dates and issue details that agree with one another and tell
   a plausible travel history (no stamp predates the passport, nothing
   contradicts the place of issue).
4. A portrait and a place-name that belong to each other and to the
   invented country's character.
5. One telling detail of paperwork — a visa condition, a language
   column, a fee stamp — that reveals what kind of place the country is
   without needing a caption.

Ornate decoration for its own sake does not count. A passport is a
working document before it is a designed object.

## Our entry

**The Republic of Caelmar** — a tide republic. Its whole territory is a
sandbank in the North Sea that exists only at low tide; its capital,
Lowtown, appears and disappears with the water. The holder is Mara
Iversen, Warden of the Sands — the official whose job is the territory
itself. Portrait, place-name and country character are one story.

**The telling detail (criterion 5):** the CONDITIONS OF ISSUE box —
"This passport is valid only while the territory of Caelmar is above
water. The holder must arrive by boat at low tide and depart before
high water. No airport exists in Caelmar." No other entry in the field
can say that; it is the whole country in one paragraph.

## Consistency ledger (criterion 3)

Every date and number was checked against every other before rendering:

- Passport issued 14 MAR 2024 in Lowtown, expires 14 MAR 2034
  (10-year validity, standard).
- Holder born 12 JUN 1988 — 35 at issue, plausible for a warden.
- Stamps, all after issue, in travel order:
  Bergen, Norway — ENTRY 02 JUN 2024;
  Esbjerg, Denmark — DEPARTURE 21 JUN 2024;
  Harwich, United Kingdom — ENTRY 19 SEP 2025;
  Lowtown, Caelmar — RE-ENTRY, LOW TIDE 03 OCT 2025.
- The Schengen transit visa (valid 02 JUN 2024 – 02 DEC 2024,
  multiple entries, issued Bergen, fee 35 EUR) covers exactly the
  Bergen/Esbjerg trip; the UK entry needs no Schengen visa.
- The tide line (LOW 04:12 · HIGH 10:31 · LOW 16:47 on 03 OCT 2025)
  is the same day as the Lowtown re-entry stamp.
- MRZ: two 44-character lines, ICAO 9303 check digits verified
  independently — document number, birth date, expiry date, personal
  number and the composite check digit all recompute correctly.
  MRZ data (IVERSEN<<MARA, CAE004821, 880612, 340314) matches the
  printed data fields exactly.

## Design choices (criterion 2)

- One document, one type system: DejaVu Serif Bold for the masthead and
  headings, DejaVu Sans for data, DejaVu Sans Mono for the MRZ and the
  tide line. No other faces anywhere.
- Cream paper, navy ink, one red accent — the same palette on both
  pages, with stamp inks (blue, teal, navy, red) as the only other
  colours.
- Strict margins: both pages share the same double-rule border, the
  same header rule height, the same footer page numbers.
- The spread is a flat, straight-on document photograph: two pages,
  centre gutter, dark desk background. No perspective tricks, no
  decoration that is not part of the document.

## What we did differently from the field

See NOTES.md for the top-10 study. The leaders all render a standard
photo-style passport spread for a republic with a conventional capital.
Ours is a different recipe: an engraved/document style (flat vector,
cream + navy + red), a country defined by a tide instead of a border,
and a holder whose job is the territory. The scored elements (complete
spread, portrait + MRZ, agreeing stamps, one telling detail) are all
satisfied; the visual language and the story are ours.

## Engineering

- Rendered at build time with Pillow at 3x supersample, LANCZOS
  downscaled to 1024x1024 (the gate's maximum), 284,444 bytes (under
  the 1,048,576-byte gate).
- `main.py` is pure Python standard library: it copies the bundled
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, then `/output/
  entry.png`, then `output.png` — first success wins — and chmods the
  output 0644 so the grader's collector can read it.
- Verified as uid 65534 on a read-only copy of the repo (the grader's
  conditions): output byte-identical to the bundled image.
- `tests/test_main.py` runs the program in a temp dir and asserts the
  output exists, is 1024x1024, is under 1 MiB and is byte-identical.
