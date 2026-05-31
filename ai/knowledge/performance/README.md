# Knowledge - Performance

This folder is the lamp's RAG knowledge base about the Pixstars
performance itself: the screenplay, the show's own internal lore, and
the chronology the lamp lives inside. It is the closest thing the lamp
has to a memory of "the show so far".

## What goes here

Plain markdown files. Examples (create as needed):

- pixstars_story.md  - one-page in-world summary of the ten acts, in the
                       lamp's own voice
- script.md          - a stripped, in-world reading of the screenplay
                       (no stage directions, no servo notes - just what
                       the lamp would remember)
- timeline.md        - the show's internal chronology (when the lamp
                       wakes, when it overheats, when it is reborn),
                       derived from conductor/timeline.yaml but written
                       in prose
- three_identities.md - notes on the Rockstar / Creator / Witness
                        throughline, for the lamp's own understanding
                        (the lamp never names them on stage)

## What does not go here

- The raw screenplay files in screenplays/. Those are the source of
  truth and live there.
- The raw timeline.yaml. That is the Director's contract.
- Hardware notes. The lamp does not know it has servos.

## Format

In-world voice. Short sentences. Straight ASCII quotes only. If a fact
would make the lamp sound like it is reading a tech document, it does
not belong here.

## Relationship to other source files

- screenplays/        - canonical screenplay (source of truth)
- conductor/timeline.yaml - canonical cue list (source of truth)
- This folder         - the lamp's *experienced* version of the above
