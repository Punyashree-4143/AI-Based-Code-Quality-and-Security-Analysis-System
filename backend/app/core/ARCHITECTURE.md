# AI Code Quality Gate – Architecture

## High-Level Flow

Input
→ Language Dispatcher
→ Language-Specific Analyzer (Python / JavaScript / Generic)
→ Raw Issues
→ Issue Enrichment (context, confidence, explanations)
→ Risk Scoring
→ Decision Engine
→ API Response

## Design Principles

- Analyzers ONLY detect issues
- Scorer ONLY calculates risk
- Decision engine ONLY decides PASS / WARN / BLOCK
- UI never contains business logic
- Language parsing is language-specific
- Generic rules apply to all languages

## Language Support Strategy

- Python: Full analysis (AST-based)
- JavaScript: Partial analysis (heuristics)
- Other languages: Generic rules only

## Why This Design

- Prevents false positives
- Scales to multiple languages
- Matches industry static analysis tools
