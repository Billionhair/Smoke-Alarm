#!/usr/bin/env bash
set -euo pipefail
trivy fs --scanners vuln,config .
