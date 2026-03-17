---
name: nlp
description: "Process text with NLP. Use when tokenizing, analyzing sentiment, extracting entities, summarizing documents, or measuring similarity."
version: "3.4.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags:
  - nlp
  - text-processing
  - sentiment
  - entities
  - summarization
  - classification
---

# nlp

Natural language processing toolbox. Tokenize text, analyze sentiment, extract entities, summarize documents, compute similarity, and classify text — all from the command line.

## Commands

### tokenize

Split text into words and sentences with frequency counts.

```bash
bash scripts/script.sh tokenize --input "The quick brown fox jumps over the lazy dog."
bash scripts/script.sh tokenize --file document.txt --json
```

### sentiment

Analyze text sentiment and return polarity (positive/negative/neutral) with confidence.

```bash
bash scripts/script.sh sentiment --input "I absolutely love this product!"
bash scripts/script.sh sentiment --file reviews.txt
```

### extract

Extract named entities (people, places, organizations, dates, numbers) from text.

```bash
bash scripts/script.sh extract --input "John Smith works at Google in Mountain View since 2020"
bash scripts/script.sh extract --file article.txt --json
```

### summarize

Generate a shorter summary of input text by extracting key sentences.

```bash
bash scripts/script.sh summarize --file long_article.txt --sentences 3
bash scripts/script.sh summarize --input "Long text here..." --ratio 0.3
```

### similarity

Compute similarity score between two texts using word overlap metrics.

```bash
bash scripts/script.sh similarity --text1 "The cat sat on the mat" --text2 "A cat was sitting on a mat"
bash scripts/script.sh similarity --file1 doc1.txt --file2 doc2.txt
```

### classify

Classify text into provided categories based on keyword matching.

```bash
bash scripts/script.sh classify --input "The stock market rallied today" --categories "finance,sports,tech,politics"
bash scripts/script.sh classify --file article.txt --categories "positive,negative,neutral"
```

## Output

Plain text by default. Use `--json` flag for JSON output. Sentiment returns polarity and score. Extract returns entity lists with types. Similarity returns a 0.0-1.0 score.


## Requirements
- bash 4+

## Feedback

Report issues or suggestions: https://bytesagain.com/feedback/

---

Powered by BytesAgain | bytesagain.com
