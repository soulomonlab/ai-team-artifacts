#!/usr/bin/env bash
# Run this script in CI or locally to produce IaC security scan outputs
set -euo pipefail
WORKDIR=${1:-.}
OUTDIR=${2:-./iac-scan-output}
mkdir -p "$OUTDIR"

echo "Running tfsec..."
if command -v tfsec >/dev/null 2>&1; then
  tfsec "$WORKDIR" --format json --out "$OUTDIR/tfsec-results.json" || true
else
  echo "tfsec not found; install with 'pip install tfsec'"
fi

echo "Running checkov..."
if command -v checkov >/dev/null 2>&1; then
  checkov -d "$WORKDIR" -o json --output-file-path "$OUTDIR/checkov-results.json" || true
else
  echo "checkov not found; install with 'pip install checkov'"
fi

echo "Running tflint..."
if command -v tflint >/dev/null 2>&1; then
  tflint --format json > "$OUTDIR/tflint-results.json" || true
else
  echo "tflint not found; install per https://github.com/terraform-linters/tflint"
fi

# Placeholder for ORT invocation
echo "ORT scan placeholder - ensure ORT is installed or run ORT via docker image"
if command -v ort >/dev/null 2>&1; then
  ort -i "$WORKDIR" -o "$OUTDIR/ort-results" || true
else
  echo "ORT not installed; see https://oss-review-toolkit.org/ for installation"
fi

echo "Scan outputs written to $OUTDIR"