export PATH := /snap/bin:$(PATH)
  
# TARGETS
lint: ## Run linter
	tox -e lint

clean: ## Remove .tox and build dirs
	rm -rf .tox/
	rm -rf venv/

push-charm-to-edge: ## Remove .tox and build dirs
	aws s3 cp license-manager.charm s3://omnivector-public-assets/charms/charm-license-manager/edge/ 

pull-charm-from-edge: ## Remove .tox and build dirs
	wget https://omnivector-public-assets.s3-us-west-2.amazonaws.com/charms/charm-license-manager/edge/license-manager.charm

pull-snap-from-edge: ## Remove .tox and build dirs
	aws s3 cp s3://omnivector-private-assets/snaps/license-manager/edge/license-manager_0.1_amd64.snap ./license-manager.snap

# Display target comments in 'make help'
help: 
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# SETTINGS
# Use one shell for all commands in a target recipe
.ONESHELL:
# Set default goal
.DEFAULT_GOAL := help
# Use bash shell in Make instead of sh 
SHELL := /bin/bash
