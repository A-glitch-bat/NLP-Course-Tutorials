"""
Alternative Text Processing Assignment (Student Version)
=======================================================

Complete the TODO sections to build a full NLTK vs Stanza comparison pipeline.
This file is intentionally scaffolded for students.
"""

import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import nltk
from nltk import ne_chunk, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

import stanza


TEXTS = [
    "Wait... did Dr. J. Smith (U.C. Berkeley) really say 'NLP is easy' at 3:30 p.m., or was it sarcasm?!",
    "Email me at first.last+nlp@uni-example.edu ASAP - unless you've already sent it via https://tinyurl.com/nlp-demo.",
    "The startup's Q4 revenue was $1.2M-ish (not audited), yet users wrote: 'app crashes on iOS17/Android14 :('",
    "I re-read the note: \"Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.\" Still parsing it...",
]

@dataclass
class PipelineResult:
    sentences: list[str]
    tokens: list[str]
    pos_tags: list[tuple[str, str]]
    lemmas: list[str]
    entities: list[tuple[str, str]]
    elapsed_s: float


class NLTKPipeline:
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()

    def process(self, text: str) -> PipelineResult:
        t0 = time.perf_counter()

        # Sentence tokenization using NLTK
        sentences = sent_tokenize(text)

        # Word tokenization using NLTK
        tokens = word_tokenize(text)

        # POS tagging using NLTK
        pos_tags_result = pos_tag(tokens)

        # Lemmatize each token using WordNetLemmatizer
        lemmas = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        # Named Entity Recognition with ne_chunk over POS tags
        tree = ne_chunk(pos_tags_result)

        # Store entities as tuples: (entity_text, entity_label)
        entities = []
        for node in tree:
            if isinstance(node, nltk.Tree):
                entity_label = node.label()
                entity_text = " ".join(word for word, pos in node.leaves())
                entities.append((entity_text, entity_label))

        return PipelineResult(
            sentences=sentences,
            tokens=tokens,
            pos_tags=pos_tags_result,
            lemmas=lemmas,
            entities=entities,
            elapsed_s=time.perf_counter() - t0,
        )


class StanzaPipeline:
    def __init__(self) -> None:
        self.stanza = stanza.Pipeline(
            lang="en",
            processors="tokenize,pos,lemma,ner",
            tokenize_pretokenized=False,
            use_gpu=False,  # safe default; remove/flip if you have GPU set up
            verbose=False,
        )

    def process(self, text: str) -> PipelineResult:
        t0 = time.perf_counter()

        # Run Stanza pipeline on text
        doc = self.stanza(text)

        # Extract sentence texts
        sentences = [s.text for s in doc.sentences]

        # Tokens, POS tags and lemmas
        tokens = []
        pos_tags_result = []
        lemmas = []
        for sentence in doc.sentences:
            #print(sentence)
            for word in sentence.words:
                #print(word) # (text, pos, lemma)
                tokens.append(word.text)

                pos_tags_result.append((word.text, word.xpos))
                
                lemmas.append(word.lemma)

        # Extract named entities as (entity_text, entity_type)
        entities = [(ent.text, ent.type) for ent in doc.ents]

        return PipelineResult(
            sentences=sentences,
            tokens=tokens,
            pos_tags=pos_tags_result,
            lemmas=lemmas,
            entities=entities,
            elapsed_s=time.perf_counter() - t0,
        )


def compare_counts(nltk_res: PipelineResult, stanza_res: PipelineResult) -> dict[str, int]:
    #print(nltk_res);print(stanza_res);print(len(nltk_res.entities))

    return {
        "sentences_nltk": len(nltk_res.sentences),
        "sentences_stanza": len(stanza_res.sentences),
        "tokens_nltk": len(nltk_res.tokens),
        "tokens_stanza": len(stanza_res.tokens),
        "entities_nltk": len(nltk_res.entities),
        "entities_stanza": len(stanza_res.entities),
    }


def visualize_token_counts(rows: list[dict[str, str]], output_path: Path) -> None:
    # Build labels: S1, S2, ... based on number of rows
    labels = [f"S{i+1}" for i in range(len(rows))]

    # Read token counts from rows and convert to int
    nltk_counts = []
    stanza_counts = []
    for row in rows:
        nltk_counts.append(int(row["tokens_nltk"]))
        stanza_counts.append(int(row["tokens_stanza"]))

    # Create a grouped bar chart (NLTK vs Stanza) and save it
    x = list(range(len(rows)))
    fig, ax = plt.subplots()

    # Requirements:
    # - X-axis: sample labels
    # - Y-axis: number of tokens
    # - title: "Token Count Comparison: NLTK vs Stanza"
    # - legend enabled
    # - save to output_path with dpi=150
    width = 0.4
    ax.bar([xi - width / 2 for xi in x], nltk_counts, width, label="NLTK")
    ax.bar([xi + width / 2 for xi in x], stanza_counts, width, label="Stanza")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Sample labels")
    ax.set_ylabel("Number of tokens")
    ax.set_title("Token Count Comparison: NLTK vs Stanza")
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)


def write_report(rows: list[dict[str, str]], output_path: Path) -> None:
    lines = [
        "# Text Processing Comparison Report",
        "",
        "Fill in the analysis prompts under each sample after running the script.",
        "",
    ]

    for i, row in enumerate(rows, start=1):
        # Add a markdown block for each sample containing:
        # - sample heading
        # - source text
        # - timings
        # - token/entity counts
        # - quick inspection previews
        # - analysis prompts
        for i, row in enumerate(rows, start=1):
            lines.extend([
                f"## Sample {i}",
                "",
                "### Source Text",
                row["text"],
                "",
                "### Timings",
                f"- NLTK time: {row['nltk_time']} seconds",
                f"- Stanza time: {row['stanza_time']} seconds",
                "",
                "### Token/entity counts",
                f"- NLTK tokens: {row['tokens_nltk']} | "
                f"Stanza tokens: {row['tokens_stanza']}",
                f"- NLTK entities : {row['entities_nltk']} | "
                f"Stanza entities: {row['entities_stanza']}",
                "",
                "### Token previews",
                f"- NLTK: {row['nltk_tokens_preview']}",
                f"- Stanza: {row['stanza_tokens_preview']}",
                "",
                "### POS previews",
                f"- NLTK: {row['nltk_pos_preview']}",
                f"- Stanza: {row['stanza_pos_preview']}",
                "",
                "### Named Entities",
                f"- NLTK: {row['nltk_entities']}",
                f"- Stanza: {row['stanza_entities']}",
                "",
                "### Analysis",
                "",
                "---",
                "",
            ])

    output_path.write_text("\n".join(lines), encoding="utf-8")


def ensure_nltk_resources() -> None:
    required = [
        "punkt",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
        "wordnet",
        "omw-1.4",
        "maxent_ne_chunker",
        "maxent_ne_chunker_tab",
        "words",
    ]
    for item in required:
        nltk.download(item, quiet=True)
        #print(item, "OK")


def run() -> None:
    print("RUNNING")
    ensure_nltk_resources()
    stanza.download("en", verbose=False)

    nltk_pipe = NLTKPipeline()
    stanza_pipe = StanzaPipeline()

    report_rows: list[dict[str, str]] = []

    for text in TEXTS:
        nltk_res = nltk_pipe.process(text)
        stanza_res = stanza_pipe.process(text)
        counts = compare_counts(nltk_res, stanza_res)

        # Append a dictionary to report_rows containing:
        row = {
            # text, nltk_time, stanza_time,
            "text": text,
            "nltk_time": f"{nltk_res.elapsed_s:.6f}",
            "stanza_time": f"{stanza_res.elapsed_s:.6f}",

            # tokens_nltk, tokens_stanza,
            # entities_nltk, entities_stanza,
            "tokens_nltk": str(counts["tokens_nltk"]),
            "tokens_stanza": str(counts["tokens_stanza"]),
            "entities_nltk": str(counts["entities_nltk"]),
            "entities_stanza": str(counts["entities_stanza"]),

            # nltk_tokens_preview, stanza_tokens_preview,
            # nltk_pos_preview, stanza_pos_preview,
            # Use previews: first 12 tokens and first 8 POS tags
            "nltk_tokens_preview": " ".join(nltk_res.tokens[:12]),
            "stanza_tokens_preview": " ".join(stanza_res.tokens[:12]),
            "nltk_pos_preview": ", ".join(f"{w}/{t}" for w, t in nltk_res.pos_tags[:8]),
            "stanza_pos_preview": ", ".join(f"{w}/{t}" for w, t in stanza_res.pos_tags[:8]),

            # nltk_entities, stanza_entities
            "nltk_entities": nltk_res.entities,
            "stanza_entities": stanza_res.entities
        }

        report_rows.append(row)

    # Call write_report using report_rows
    report_path = Path("text_processing_alternative_report.md")
    write_report(report_rows, report_path)

    # Call visualize_token_counts using report_rows
    plot_path = Path("token_count_comparison.png")
    visualize_token_counts(report_rows, plot_path)

    print("DONE")


if __name__ == "__main__":
    run()
