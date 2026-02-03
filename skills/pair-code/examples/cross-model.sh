#!/bin/bash
# Example: Cross-model review workflow
# Gemini implements, Claude reviews for diverse perspectives

~/Tools/pair-code "add input validation for email and password fields" \
  src/auth/login.py \
  -i gemini \
  -r claude \
  --max-rounds 3
