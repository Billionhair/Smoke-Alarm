#!/usr/bin/env bash
set -euo pipefail
syft . -o json > sbom.json
