IMAGE_NAME ?= donburi/jira-bot
BUILD_TAG ?= latest

build:
	echo ${IMAGE_NAME}
	DOCKER_BUILDKIT=1 docker build -t ${IMAGE_NAME}:${BUILD_TAG} .
