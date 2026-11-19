# Scoring Methodology

## Advanced Ranking Formula

The advanced API uses:

Score = 0.55M + 0.35C + 0.10E - G

Where:

- M = Semantic similarity between job description and resume.
- C = Required-skill coverage.
- E = Experience score.
- G = Missing-skill gap penalty.

## Semantic Similarity

The system uses Sentence Transformers with the
all-MiniLM-L6-v2 model.

The job description and resume are converted into embeddings.
Cosine similarity measures their semantic similarity.

## Required-Skill Coverage

Coverage = Matched required skills / Total required skills.

If there are no required skills, the implementation uses
a denominator of 1.

## Experience Score

If the minimum experience requirement is zero or less,
the experience score is 1.

Otherwise:

Experience score = min(1, candidate experience / minimum required experience).

## Missing-Skill Penalty

Gap penalty = 0.10 x Number of missing required skills.

## Original CLI Scoring

The original CLI matcher uses a separate formula:

Final score = (0.60 x TF-IDF similarity
               + 0.40 x skill coverage) x 100

               The CLI and advanced API scoring methods are different.

               ## Important Note

               The advanced API score is not a probability of being hired
               or a scientifically validated measure of candidate quality.
