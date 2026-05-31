# Knowledge - Disney

This folder is the lamp's RAG (retrieval-augmented generation) knowledge
base about Walt Disney and the early Disney studio. The lamp queries it
when something on stage triggers a Disney reference, or when the Walt
agent is loaded.

## What goes here

Plain markdown files, one topic per file, short and quotable. Examples
(not yet written - create as needed):

- walt_quotes.md     - short, verifiable Walt quotes, one per line
- disney_history.md  - studio timeline up to roughly 1966, dates only
- creativity.md      - notes on hand-drawn animation, pencil tests, the
                       "imagineering" mindset
- mickey.md          - origin of the character, the 1928 short, the glove
- snow_white.md      - the first feature, why it mattered

## What does not go here

- Anything written after 1966 (the show's Walt does not know it).
- Disney corporate / parks / IP material from the modern company.
- Long essays. Keep files under ~50 lines so retrieval stays sharp.

## Format

Each file should be readable on its own. Use plain prose or short
bulleted notes. No YAML front-matter. Straight ASCII quotes only.

## Indexing

Files in this folder are indexed by the RAG layer at lamp startup. To
force a re-index, restart the lamp agent.
