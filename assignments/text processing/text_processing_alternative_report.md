# Text Processing Comparison Report

## Sample 1

### Source Text
Wait... did Dr. J. Smith (U.C. Berkeley) really say 'NLP is easy' at 3:30 p.m., or was it sarcasm?!

### Timings
- NLTK time: 3.290836 seconds
- Stanza time: 0.409297 seconds

### Token/entity counts
- NLTK tokens: 27 | Stanza tokens: 26
- NLTK entities : 2 | Stanza entities: 3

### Token previews
- NLTK: Wait ... did Dr. J. Smith ( U.C . Berkeley ) really
- Stanza: Wait ... did Dr. J. Smith ( U.C. Berkeley ) really say

### POS previews
- NLTK: Wait/NN, .../:, did/VBD, Dr./NNP, J./NNP, Smith/NNP, (/(, U.C/NNP
- Stanza: Wait/VB, .../,, did/VBD, Dr./NNP, J./NNP, Smith/NNP, (/-LRB-, U.C./NNP

### Named Entities
- NLTK: [('Wait', 'GPE'), ('Berkeley', 'PERSON')]
- Stanza: [('J. Smith', 'PERSON'), ('U.C. Berkeley', 'ORG'), ('3:30 p.m.', 'TIME')]

### Analysis
- Large initialization delay for NLTK, which Stanza does not have. Slightly different token counting, POS error for NLTK. NLTK also makes mistakes with named entities, adding "Wait" and missing "J. Smith". Overall, Stanza performs better.

---

## Sample 2

### Source Text
Email me at first.last+nlp@uni-example.edu ASAP - unless you've already sent it via https://tinyurl.com/nlp-demo.

### Timings
- NLTK time: 0.634446 seconds
- Stanza time: 0.443778 seconds

### Token/entity counts
- NLTK tokens: 19 | Stanza tokens: 14
- NLTK entities : 1 | Stanza entities: 0

### Token previews
- NLTK: Email me at first.last+nlp @ uni-example.edu ASAP - unless you 've already
- Stanza: Email me at first.last+nlp@uni-example.edu ASAP - unless you 've already sent it

### POS previews
- NLTK: Email/VB, me/PRP, at/IN, first.last+nlp/JJ, @/JJ, uni-example.edu/JJ, ASAP/NNP, -/:
- Stanza: Email/VB, me/PRP, at/IN, first.last+nlp@uni-example.edu/ADD, ASAP/FW, -/,, unless/IN, you/PRP

### Named Entities
- NLTK: [('ASAP', 'ORGANIZATION')]
- Stanza: []

### Analysis
- Stanza has slightly better time. NLTK splits the mail unnecessarily and detects a false named entity, leading to some POS issues. Stanza does better.

---

## Sample 3

### Source Text
The startup's Q4 revenue was $1.2M-ish (not audited), yet users wrote: 'app crashes on iOS17/Android14 :('

### Timings
- NLTK time: 0.678751 seconds
- Stanza time: 0.441818 seconds

### Token/entity counts
- NLTK tokens: 24 | Stanza tokens: 27
- NLTK entities : 0 | Stanza entities: 1

### Token previews
- NLTK: The startup 's Q4 revenue was $ 1.2M-ish ( not audited )
- Stanza: The startup 's Q4 revenue was $ 1.2 M - ish (

### POS previews
- NLTK: The/DT, startup/NN, 's/POS, Q4/NNP, revenue/NN, was/VBD, $/$, 1.2M-ish/JJ
- Stanza: The/DT, startup/NN, 's/POS, Q4/NNP, revenue/NN, was/VBD, $/$, 1.2/CD

### Named Entities
- NLTK: []
- Stanza: [('$1.2M', 'MONEY')]

### Analysis
- NLTK takes slightly longer. Different tokenization around money, which Stanza understands as a named entitiy, otherwise both correct.

---

## Sample 4

### Source Text
I re-read the note: "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo." Still parsing it...

### Timings
- NLTK time: 0.673732 seconds
- Stanza time: 0.324377 seconds

### Token/entity counts
- NLTK tokens: 20 | Stanza tokens: 20
- NLTK entities : 3 | Stanza entities: 3

### Token previews
- NLTK: I re-read the note : `` Buffalo buffalo Buffalo buffalo buffalo buffalo
- Stanza: I re-read the note : " Buffalo buffalo Buffalo buffalo buffalo buffalo

### POS previews
- NLTK: I/PRP, re-read/VBP, the/DT, note/NN, :/:, ``/``, Buffalo/NNP, buffalo/NN
- Stanza: I/PRP, re-read/VBP, the/DT, note/NN, :/:, "/``, Buffalo/NNP, buffalo/NNP

### Named Entities
- NLTK: [('Buffalo', 'PERSON'), ('Buffalo', 'PERSON'), ('Buffalo', 'PERSON')]
- Stanza: [('Buffalo', 'GPE'), ('Buffalo', 'GPE'), ('Buffalo', 'GPE')]

### Analysis
- Stanza has better time. NLTK stays consistent with quote marks, where Stanza doesn't. Differences in POS tagging and approach to NE, but both ok.

---
