#!/usr/bin/env python3
"""Generate evidence-first revise prompts; historical per-article directives are retired."""
from editorial_prompts import main

if __name__ == "__main__":
    main("revise")
