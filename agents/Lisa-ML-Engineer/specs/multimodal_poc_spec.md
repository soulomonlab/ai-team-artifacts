# Multimodal POC: Text + Image for Product Flow

## Situation
We need a prototype feature that accepts both user text and product images to support one core product workflow (e.g., product search, issue triage, or QA). The goal is to validate feasibility, produce a minimal demo, and recommend a production approach.

## Scope
- Deliverables: dataset sample (text+image pairs), model selection recommendation, and runnable demo script.
- Target workflow for POC: relevance-matching between user text and product images (text->image retrieval & classification of intent).
- Constraints: prototype must be executable locally, use open-source components (HuggingFace/PyTorch), and be reproducible.

## Acceptance criteria
- Sample dataset (>=100 synthetic pairs recommended for next stage; we provide a 6-entry sample for demo).
- Demo script that runs end-to-end locally and returns top-k image matches for a text query (p95 latency <500ms on dev machine expected).
- Clear model recommendation with trade-offs and training plan.

## Data requirements
- For robust fine-tuning: 5k–50k matched (text, image) pairs depending on task complexity.
- Labels: for retrieval — pairs are positive/negative; for classification — intent labels (e.g., "search", "report_issue", "compare").
- Metadata: product_id, image_id, timestamp, device, locale.

## Evaluation metrics
- Retrieval: Recall@1/5, MRR
- Classification: Accuracy, Precision/Recall/F1 per class
- Latency: p95 inference <50ms (real-time) or <500ms for prototype
- Resource: model size, GPU memory

## Candidate approaches (high level)
1) CLIP (contrastive) — fine-tune or linear probe
   - Pros: strong text-image alignment, efficient embeddings, low-latency retrieval
   - Cons: limited generative reasoning
2) BLIP / BLIP-2 or Flamingo — multimodal generation/understanding
   - Pros: better at reasoning and complex QA
   - Cons: heavier, higher latency/cost
3) Dual-encoder image+text retrieval + RAG for context
   - Pros: combines fast retrieval with deeper text LLM reasoning
   - Cons: additional infra for RAG

## Recommendation (short)
Start with CLIP-based dual-encoder retrieval for the POC: fastest to prototype, low infra requirements, good retrieval accuracy. If later we need generative reasoning (explainability, step instructions), explore BLIP-2 or RAG.

## Training plan (CLIP fine-tune)
- Preprocessing: standard image resize/crop, normalization; text lowercasing, tokenization.
- Optimizer: AdamW, lr 1e-5 to 5e-5, batch 64 (accumulate if GPU limits).
- Epochs: 3-10 (monitor val Recall@1).
- Logging: MLflow for metrics & artifacts.

## Demo plan
- Provide a minimal inference script that computes image and text embeddings and returns nearest neighbors (cosine similarity).
- Use sample JSONL dataset for demo.
- Deliverable: output/code/ml/multimodal_demo_inference.py

## Next steps for data (requested to #ai-data)
- Provide 3 months of product images + user search logs (JSONL or parquet)
- Provide labels for at least 5k positive pairs or clear labeling guidelines

## Files created in this POC
- output/specs/multimodal_poc_spec.md
- output/data/multimodal_sample.jsonl
- output/code/ml/multimodal_demo_inference.py
- output/reports/multimodal_model_recommendation.md

