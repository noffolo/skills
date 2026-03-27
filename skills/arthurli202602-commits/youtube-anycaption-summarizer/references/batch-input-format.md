# Batch Input Format

Use a plain text file with one YouTube URL per line.

Example:

```text
https://www.youtube.com/watch?v=RX-fQTW2To8
https://www.youtube.com/watch?v=657wlbtrzG8
```

## Rules
- Ignore blank lines.
- Ignore lines starting with `#`.
- Process URLs sequentially in file order.
- Create one dedicated subfolder per video under the chosen parent output folder.
- Treat each item as an independent workflow run with its own transcript, summary placeholder, and cleanup step.

## Per-item workflow in batch mode
For each URL, the main workflow should:
1. fetch metadata
2. derive sanitized output paths
3. try subtitle-first extraction
4. fall back to media download + Whisper transcription when needed
5. write the raw transcript markdown
6. write the summary placeholder markdown
7. clean intermediates unless explicitly told to keep them

After deterministic processing, summarize each item sequentially and run the finalizer script for each finished summary.

## Failure handling
- By default, a failure stops the batch.
- With `--continue-on-error`, record the failure and continue with later URLs.
- Report both successes and failures clearly at the end.
