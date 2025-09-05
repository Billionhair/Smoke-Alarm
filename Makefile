 codex/set-up-git-auto-resolve-and-checks
.PHONY: pr setup


 main
pr:
	@bash scripts/pr-preflight.sh

setup:
	@echo "Configuring repo defaults..."
	@git config pull.rebase true
	@git config rebase.autostash true
	@git config rerere.enabled true
	@git config rerere.autoUpdate true
	@git config merge.conflictstyle zdiff3
	@git config merge.renormalize true
