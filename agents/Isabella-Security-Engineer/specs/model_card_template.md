# Model Card Template

Purpose
- Provide transparent, structured information about each deployed model to support governance, user understanding, and compliance.

Model Overview
- Model name:
- Model id:
- Version:
- Owner/Team:
- Purpose / Intended use:
- License:
- Date trained:

Technical Details
- Architecture: (e.g., XGBoost, transformer-based)
- Input features: list with types and preprocessing steps
- Output: classes/metrics, probability ranges
- Training data: data sources, collection date ranges, sizes, sampling notes, any known biases
- Data lineage: dataset versions, preprocessing pipelines

Performance
- Evaluation metrics: accuracy, precision, recall, AUC, F1 (on test sets)
- Evaluation datasets: description, size, demographic breakdown if applicable
- Limitations: known failure modes and contexts where model underperforms
- Drift monitoring plan: metrics tracked and alert thresholds

Security & Privacy
- PII handling: fields collected, masking/anonymization applied
- Adversarial considerations: known vulnerabilities (e.g., membership inference, model inversion)
- Access controls: who can query model and who can access logs
- Risk assessment summary: top 3 risks and mitigations

Operationalization
- Deployment environment: staging/prod, container images, orchestration
- Monitoring: latency, throughput, error rates, model quality metrics
- Retraining cadence: triggers for retrain (drift thresholds, periodic)
- Rollback strategy

Audit & Compliance
- Logging: what inputs/outputs are logged and retention periods
- Responsible contact for data subject requests
- Regulatory considerations: GDPR, HIPAA (if applicable)

Metadata & Links
- Model artifacts: S3 path, container image tag
- Training code: repo link
- Evaluation notebooks
- Related tickets / PRs

Revision History
- Date | Author | Change summary

Instructions for use
- Each model must have a model card in the registry before production deployment.
- Security and privacy sections must be signed off by Security and Privacy teams (Isabella + Privacy lead).
