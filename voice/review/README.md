# Voice Review Queue

This folder is the human-in-the-loop checkpoint for the Pixstars lamp voice.

## Buckets

- `approved/`
- `needs_human_review/`
- `rejected/`

## Flow

1. Candidate WAVs are rendered into `voice/output/candidates/`
2. The evaluator writes `voice/orchestration/state/evaluation.csv`
3. The review queue script distributes candidates into:
   - approved
   - needs_human_review
   - rejected
4. The publish step promotes only approved files to `voice/output/final_wav/`

## Why this exists

Your show benefits from automation, but the lamp is a character. This queue ensures you can keep artistic control where it matters most.
