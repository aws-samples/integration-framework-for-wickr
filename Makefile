.SHELL := /usr/bin/bash
TARGETS_DOCS_FILE  := "assets/targets.md"

help:
	@grep -E '^[a-zA-Z_-_\/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dependencies: ## Add Python dependencies
	pushd functions/api/python; pip3 install -r requirements.txt -t ./ ; popd 

debug/incident: ## Run the Lambda IR function
	@sam build APIExample
	@sam local invoke APIExample -e events/command_control_finding_from_guard_duty.json --parameter-overrides WickrUrl="$(WickrAPIUrl)" WickrApiKey=$(WickrApiKey)

deploy: dependencies ## Deploy the SAM app (once deploy/guided has been runn to generate a samconfig.yaml)
	sam deploy 

deploy/guided: dependencies ## Guided deployment
	sam deploy \
	--template-file template.yaml \
	--stack-name AWIF \
	--capabilities CAPABILITY_IAM \
	--no-confirm-changeset \
	--parameter-overrides ParameterKey=WickrUrl,ParameterValue=$(WickrAPIUrl) ParameterKey=WickrApiKey,ParameterValue=$(WickrApiKey) \
	--guided

deploy/custom: dependencies ## Deploy the SAM app with custom params
	sam deploy \
	--template-file template.yaml \
	--stack-name AWIF \
	--capabilities CAPABILITY_IAM \
	--s3-bucket bucket-name \
	--parameter-overrides ParameterKey=WickrUrl,ParameterValue=$(WickrAPIUrl) ParameterKey=WickrApiKey,ParameterValue=$(WickrApiKey)

delete: ## Delete application
	sam delete

package: ## Create CF output
	sam build
	sam package --output-template-file awif.yaml --s3-bucket bucketname --debug

createdocs/targets: # Create list of make targets in Markdown format
	@echo Auto creating README.md....
	@rm -rf $(TARGETS_DOCS_FILE)
	@echo "## Makefile Targets" >> $(TARGETS_DOCS_FILE)
	@echo -e "The following targets are available: \n" >> $(TARGETS_DOCS_FILE)
	@echo '```' >> $(TARGETS_DOCS_FILE)
	@grep -E '^[a-zA-Z_-_\/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\%-30s\ %s\n", $$1, $$2}' >> $(TARGETS_DOCS_FILE)
	@echo '```' >> $(TARGETS_DOCS_FILE)