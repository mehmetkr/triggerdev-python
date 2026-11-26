#!/usr/bin/env bash
set -euo pipefail

# Generate baseline Pydantic v2 models from the pinned OpenAPI spec.
# Output is a single file for manual inspection; hand-tuned models live
# in src/triggerdev/types/ and are the source of truth.

SPEC="spec/v3-openapi.yaml"
OUT="generated_models.py"

datamodel-codegen \
    --input "$SPEC" \
    --output "$OUT" \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.10

echo "Generated $OUT from $SPEC"
echo "Next: diff against src/triggerdev/types/ and merge changes manually."
