"""Script: evaluate agent quality against a golden dataset.

This is an operational script, not part of the installable package.
Run it to measure how well your agent answers a curated set of questions.

Usage:
    uv run python scripts/evaluate_agent.py
    # or: make evaluate

Steps to implement:
    1. Load a golden dataset from data/samples/ (questions + expected answers).
    2. For each question, run the agent and collect the response.
    3. Compute evaluation metrics (e.g., faithfulness, relevancy, BLEU/ROUGE).
    4. Output a summary report to stdout or a file.
    5. Optionally send traces to your monitoring backend (Langfuse, etc.).

Recommended evaluation libraries:
    - RAGAS (pip install ragas) — RAG-specific metrics
    - DeepEval (pip install deepeval) — LLM evaluation framework
    - Custom scoring with your own rubric

Example dataset format (data/samples/eval_set.json):
    [
      {
        "question": "What is the main topic?",
        "expected_answer": "The main topic is ...",
        "context_doc_ids": ["doc_1", "doc_2"]
      }
    ]
"""

# TODO: Implement the evaluation script for your agent.
