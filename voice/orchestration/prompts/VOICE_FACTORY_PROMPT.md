# Voice Factory Prompt

Run the Pixstars lamp voice workflow end to end.

1. Read `voice/orchestration/state/episode_sources.txt`
2. Extract the lamp's spoken lines into `voice/data/dialogue.csv`
3. Build the dialogue manifest
4. Create the render queue
5. Generate candidate outputs for missing lines
6. Evaluate all new candidates
7. Publish approved assets to `voice/output/final_wav/`
8. Regenerate `ardour/cues/cue_manifest.csv`
9. Summarize what changed, what was approved, and what still needs review
