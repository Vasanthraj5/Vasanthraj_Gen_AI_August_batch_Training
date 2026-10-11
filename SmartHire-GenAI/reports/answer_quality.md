# SmartHire GenAI Evaluation

## Retrieval relevance
Measure whether retrieved jobs match the candidate's target role and skills.

Suggested metrics:
- Top-5 relevance
- Skill keyword hit rate
- Manual relevance review

## Mentor quality
Evaluate:
- correctness
- grounding in retrieved context
- helpfulness
- refusal when information is absent

## Prompt comparison
Record before/after prompt versions and compare:
- JSON validity
- extraction completeness
- hallucination rate
- usefulness of CV suggestions

## Guardrail testing
Test:
- empty input
- unsafe/off-topic input
- career questions
- questions whose answer is absent from the corpus

## Deployment
Record:
- GitHub repository
- deployed Streamlit URL
- screenshots
- final test results
