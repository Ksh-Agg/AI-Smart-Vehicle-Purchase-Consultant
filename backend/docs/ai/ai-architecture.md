# SVPC AI Recommendation Pipeline Specification

## 1. Pipeline Overview
The AI recommendation pipeline scores and ranks vehicles against a user preference profile dynamically generated from standard intake questionnaires.

## 2. Execution Sequence
### 2.1 Questionnaire Data Ingestion (`app/schemas`)
Pydantic parsing of intake answers.
### 2.2 Feature Preprocessing & Scaling (`app/ai/preprocessing`)
Min-Max scaling and mapping of physical features to normalized score bounds.
### 2.3 Preference Bound Inference (`app/ai/engine`)
Generates dynamic bounds based on customer preference inputs.
### 2.4 Fuzzy Logic Scoring (`app/ai/fuzzy`)
Fuzzy rating of spec fields against preference ranges.
### 2.5 Dynamic Weight Allocation (`app/ai/engine`)
Allocates scoring weights based on user-defined priority levels (high, medium, low).
### 2.6 Multi-Attribute Vehicle Ranking (`app/ai/engine`)
Computes aggregate ranking scores.
### 2.7 Natural Language Explanation Generation (`app/ai/providers`, `app/ai/prompts`)
Sends ranked results and scores to the LLM explanation layer for human-readable reasons.

## 3. Artifact & Asset Management (`artifacts/`)
## 4. AI Provider Abstraction Interface (`app/ai/providers`)

---

## Related Documentation
- [System Architecture Specification](../architecture/system-architecture.md)
