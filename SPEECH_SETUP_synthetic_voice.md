# SPEECH_SETUP.md

## Synthetic voice creation for a lamp character, with Ardour-based MIDI triggering and E.T.-inspired character shaping

## Purpose

This document explains how to build a synthetic character voice from scratch, generate dialogue as audio, trigger that audio in Ardour from MIDI, and shape the result toward a small, fragile, emotional, extraterrestrial character quality.

This version assumes you want to go straight for synthetic voice creation, not just generic cloud TTS plus effects.

---

## 1. Creative target

The goal is not to copy the exact original film voice of E.T.

The goal is to create a voice that is:

- small
- vulnerable
- curious
- slightly raspy
- emotionally warm
- believable as a living being inside the lamp

That gives you the artistic effect you want while building an original character voice identity.

---

## 2. Key insight: why this should start with synthetic voice design

### Insight A - OpenVoiceOS synthetic-voice pipeline

The OpenVoiceOS article “Making Synthetic Voices From Scratch” describes a pipeline where a base voice is used to generate synthetic speech/text pairs, that speech is transformed into a new target voice through voice conversion, and a compact offline model is then trained on the resulting synthetic dataset.

Reference:
https://blog.openvoiceos.org/posts/2025-06-26-making-synthetic-voices-from-scratch

### Insight B - the E.T.-style voice works because of human imperfection

The YouTube reference about the voice behind E.T. reinforces that the emotional effect comes from fragility, rasp, imperfection, and breath, not just pitch shifting.

Reference:
https://youtube.com/shorts/KcSDmKQoWCs

## Conclusion

So the correct philosophy is:

Synthetic voice creation first -> performance shaping second

not:

generic TTS -> extreme FX -> hope for the best

---

## 3. Recommended architecture

Use this pipeline:

Synthetic voice model -> render WAV dialogue -> Ardour -> MIDI trigger -> character FX bus -> lamp speaker

That gives you:

- repeatable dialogue generation
- offline capability
- consistent voice identity
- fast rehearsal workflow
- high reliability in performance

---

## 4. Best toolchain choice

## Recommended primary engine: Piper-style local voice model

For this project, the most practical target is a compact local voice model that can be rendered into WAV quickly and run offline. Piper is explicitly positioned as a fast, local neural text-to-speech system, and its training documentation and samples make it a strong fit for a self-hosted performance workflow.

References:
- https://github.com/rhasspy/piper
- https://github.com/rhasspy/piper/blob/master/TRAINING.md
- https://rhasspy.github.io/piper-samples/

## Recommended research / experimentation engine: Coqui TTS

Coqui TTS is useful as the broader experimentation and model-training environment because it provides tooling for training new models, fine-tuning, and voice cloning workflows.

References:
- https://coqui-tts.readthedocs.io/
- https://coqui-tts.readthedocs.io/en/latest/cloning.html
- https://github.com/coqui-ai/tts

## Practical recommendation

For your performance project:

- use Coqui TTS or related tooling for experimentation and model preparation,
- aim to produce a compact local voice asset suitable for offline generation,
- use Ardour for triggering, playback, and theatrical shaping.

---

## 5. The synthetic-voice strategy

There are three ways to create a custom character voice.

## Strategy 1 - Full training from a real recorded speaker

Not the route you asked for, but listed for completeness.

## Strategy 2 - Clone from a short real reference

Powerful, but it depends on an actual donor voice.

## Strategy 3 - Synthetic voice from scratch

This is the route to use here.

The idea is:

1. start from an existing synthetic base voice,
2. generate lots of speech,
3. transform that speech toward the target character,
4. train or fine-tune a compact model on the transformed data,
5. use that new model as your lamp voice.

This is the OpenVoiceOS-style idea and is the best conceptual match for your goal.

---

## 6. Target voice design specification

Before building anything technical, define the voice as a character.

## Lamp voice target profile

- perceived age: childlike / ageless
- body scale: tiny
- tone: warm, emotionally exposed
- articulation: slightly hesitant
- breath: audible at times
- rasp: subtle
- pacing: slow to medium-slow
- pitch: moderately elevated
- formant/body: slightly smaller than natural human speech
- intelligibility: clear enough for theatre, not cartoonish

## Avoid

- chipmunk sound
- metallic robot sound
- over-polished assistant voice
- excessive vocoder character
- comedy-style alien voice

---

## 7. Synthetic dataset creation workflow

This is the core build path.

## Step 1 - Pick a synthetic base voice

Choose a synthetic base voice that is already closer to these traits:

- softer delivery
- not too bright
- not too deep
- slightly breathy if possible
- emotionally neutral or gentle

Do not start from a hard, glossy, announcer-like voice.

## Step 2 - Generate a broad text set

Generate several hundred to several thousand lines of text with varied phonemes and emotional phrasing.

Include:

- short emotional phrases
- neutral sentences
- vowels and soft consonants
- whispered-feeling lines
- curious / confused / affectionate phrases

Examples:

- Hello...
- I am here...
- Please wait...
- Why did you go?
- I remember you.
- The light is warm.
- I was afraid.
- Stay with me.

## Step 3 - Render synthetic speech from the base voice

Export the generated lines as WAV files.

Recommended format:

- WAV
- mono
- 22.05 kHz or 24 kHz during model work if required by your pipeline
- 48 kHz exports later for Ardour session use

## Step 4 - Transform the dataset toward the target character

Now create the character coloration.

This is where the OpenVoiceOS concept matters:
you do not merely keep the base voice as-is; you transform it toward your target identity.

Target transforms:

- slight pitch raise
- slight formant raise
- mild rasp
- breathiness
- small instability
- softened edges
- emotional hesitation

You can do this transformation in an automated preprocessing stage or through batch audio processing, depending on the tools you use.

## Step 5 - Curate the result

Reject samples that are:

- too robotic
- too harsh
- too bright
- too distorted
- too comic
- too human-adult

Keep only the voice identity you want repeated.

## Step 6 - Train or fine-tune the new compact voice model

Use the transformed synthetic dataset to train a compact model or fine-tune from an existing checkpoint. The OpenVoiceOS article explicitly describes this compact-model approach, with the goal of running fully offline.

---

## 8. Recommended practical build route

If you want the highest chance of success without turning this into a research project, use this staged route.

## Phase A - Prototype the voice identity

Use existing TTS plus batch processing to discover the character.

Output:
- 20 to 50 test lines
- 3 to 5 tonal variants
- one preferred character profile

## Phase B - Build a synthetic training set

Generate a large synthetic corpus from the base voice and transform it toward the target.

Output:
- curated dataset
- final target settings
- metadata ready for training

## Phase C - Train the compact local model

Train or fine-tune your local voice.

Output:
- one reusable lamp voice model

## Phase D - Render performance lines

Use the trained synthetic voice to render all show dialogue as WAV files.

Output:
- stable, reusable cue library

## Phase E - Bring it into Ardour

Use Ardour for triggering and stage shaping.

---

## 9. Dialogue writing for a believable creature voice

Even with a great synthetic model, the text matters enormously.

Write lines for speech, not for reading.

## Good habits

- Keep lines short
- Use ellipses for hesitation
- Use punctuation for breath and timing
- Avoid complex sentence structures
- Let the character search for words

## Better examples

- Hello...
- I know you.
- Please... stay.
- I was lost.
- The light... is you.
- I remember... the music.

## Less good examples

- I would like to inform you that I have now become operational.
- Hello, I am a friendly being who resides inside this lamp.

---

## 10. Render format for Ardour

Once the model is ready, render final show lines as:

- WAV
- 48 kHz
- 24-bit if convenient
- mono unless you have a strong reason otherwise

Suggested naming:

- lamp_01_hello.wav
- lamp_02_stay.wav
- lamp_03_why_did_you_leave_me.wav
- lamp_04_rebirth.wav

---

## 11. Bringing the synthetic voice into Ardour

Ardour is the performance layer, not the primary speech generator.

Use it for:

- playback
- triggering
- timing
- mixing
- scene consistency
- small final character enhancements

Create at least:

1. VOICE_PLAYER
2. VOICE_FX
3. LAMP_OUT

---

## 12. MIDI triggering in Ardour

There are two good routes.

## Route A - Cue / clip triggering from a MIDI controller

Best for:
- live performance
- manual triggering
- one pad per line

Workflow:

1. import rendered voice WAV files,
2. place them in Ardour cue slots,
3. assign MIDI notes or pads via MIDI Learn,
4. trigger them live.

## Route B - Sampler triggered by a MIDI track or MIDI file

Best for:
- exact sequencing
- timeline automation
- repeatable shows

Workflow:

1. load voice WAV files into a sampler plugin,
2. assign each line to a MIDI note,
3. create or import a MIDI file,
4. let the MIDI notes trigger the speech samples.

This is the most literal way to have a MIDI file trigger the voice.

---

## 13. Final character shaping in Ardour

Now that the voice model itself already contains much of the identity, Ardour should only provide light finishing touches.

That is a major change from the previous workflow.

You no longer want Ardour to do all the heavy lifting.
You want Ardour to preserve and enhance the synthetic voice identity.

## Recommended chain

1. Gain trim
2. Pitch/Formant plugin if only a tiny final adjustment is needed
3. EQ
4. Light compression
5. Tiny ambience
6. Optional subtle texture
7. Output trim

---

## 14. Best Ardour plugin choices for the final voice polish

## Best main shaper: Graillon 3

Graillon 3 remains the strongest practical plugin for final voice shaping because it offers pitch shifting, formant shifting, pitch correction, and additional vocal effects in one place.

Reference:
https://www.auburnsounds.com/products/Graillon.html

Use it gently now, because the synthetic model should already carry much of the character.

### Starting settings
- pitch shift: +1 to +3 semitones, not more unless truly needed
- formant: slight upward shift
- pitch correction: very mild or off
- chorus: tiny amount only
- compression: light if used inside the plugin

## Offline alternate generation: Rubber Band based pitch processing

Rubber Band is designed for high-quality pitch shifting and time stretching and is useful for rendering alternate line versions offline.

Reference:
https://breakfastquay.com/rubberband/

Use it to test variants such as:

- more fragile
- more magical
- more wounded

## Not the main transformation tool: x42 Auto Tune

x42 Auto Tune is useful for pitch correction but is not the best primary tool for this kind of creature-voice transformation because it does not provide formant correction.

Reference:
https://x42-plugins.com/x42/x42-autotune

---

## 15. How to approach the E.T.-inspired sound technically

The human-origin insight matters here.

The quality people associate with that kind of voice is not just “small.”
It is:

- fragile
- breath-led
- slightly rasped
- effortful
- intimate
- emotionally exposed

## Technical translation

### Do
- use a softer source voice
- preserve tiny imperfections
- allow breath and pause
- keep mild instability
- use only modest pitch lift
- keep ambience tiny

### Do not
- hard-tune it
- over-compress it
- over-brighten it
- over-formant it
- use a big sci-fi effect stack

## Optional enhancement layer

If the synthetic voice is still too clean, add one or two of these in tiny amounts:

- soft saturation
- breath layer on a parallel track
- micro volume automation
- subtle short delay
- very small chorus

---

## 16. Speaker realism: make the voice come from the lamp

If possible, route the lamp voice to a physical speaker inside or near the lamp body.

That gives you the strongest illusion that the lamp itself is alive.

## Output advice

- keep the voice mostly mono
- remove deep lows
- keep the midrange articulate
- avoid huge stereo widening
- send only as much to the main PA as needed

A physically smaller sounding source often helps the illusion.

---

## 17. Recommended build recipe for your project

This is the most practical version.

## Voice creation recipe

1. choose a soft synthetic base voice,
2. generate a synthetic corpus,
3. transform it toward:
   - slightly higher
   - slightly smaller
   - slightly raspier
   - emotionally softer
4. curate the result,
5. train or fine-tune the compact local model,
6. render your final dialogue WAV files.

## Performance recipe

1. import final WAV files into Ardour,
2. use cue slots for live lines,
3. use sampler + MIDI track for sequenced lines,
4. place Graillon 3, EQ, compression, and tiny ambience on the voice bus,
5. output to lamp speaker.

---

## 18. Example emotional voice banks

Render multiple states of the same line.

Example:

- lamp_01_hello_curious.wav
- lamp_01_hello_wounded.wav
- lamp_01_hello_reborn.wav

Map them to different cues or notes.

This gives the lamp emotional range without changing the underlying character identity.

---

## 19. Quick-start checklist

- [ ] Define the character voice profile
- [ ] Choose a synthetic base voice
- [ ] Generate a synthetic text/audio corpus
- [ ] Transform the corpus toward the target character
- [ ] Curate the transformed dataset
- [ ] Train or fine-tune the compact offline voice model
- [ ] Render final show dialogue as WAV
- [ ] Create Ardour session at 48 kHz
- [ ] Import voice WAV files
- [ ] Configure cue or sampler triggering
- [ ] Map MIDI
- [ ] Add very light final shaping
- [ ] Route to lamp speaker
- [ ] Rehearse with movement and lighting

---

## 20. Final recommendation

For your lamp project, the strongest approach is to stop thinking in terms of generic TTS plus lots of effects and instead create a dedicated synthetic voice identity first. The OpenVoiceOS approach shows that a synthetic pipeline can be used to generate, transform, and train a compact offline voice from synthetic material, while the E.T. voice insight reminds you that emotional fragility, rasp, breath, and imperfection are what make such a voice feel alive. Build the voice model first, then let Ardour handle triggering, timing, and only light final shaping. That will give your lamp the best chance of sounding like a real character rather than a processed effect.

---

## Source references

- OpenVoiceOS synthetic voice article: https://blog.openvoiceos.org/posts/2025-06-26-making-synthetic-voices-from-scratch
- YouTube E.T.-voice reference: https://youtube.com/shorts/KcSDmKQoWCs
- Piper repository: https://github.com/rhasspy/piper
- Piper training documentation: https://github.com/rhasspy/piper/blob/master/TRAINING.md
- Piper voice samples: https://rhasspy.github.io/piper-samples/
- Coqui TTS docs: https://coqui-tts.readthedocs.io/
- Coqui cloning docs: https://coqui-tts.readthedocs.io/en/latest/cloning.html
- Coqui repository: https://github.com/coqui-ai/tts
- Graillon 3: https://www.auburnsounds.com/products/Graillon.html
- Rubber Band: https://breakfastquay.com/rubberband/
- x42 Auto Tune: https://x42-plugins.com/x42/x42-autotune
