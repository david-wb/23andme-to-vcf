IMAGE_NAME=davidwb/23andme-to-vcf
MAJOR=1
MINOR=0
PATCH=0

all: default

default: build

build:
	docker build . -t ${IMAGE_NAME} --no-cache \
		--build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		--build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		--build-arg AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
	docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${MAJOR}.${MINOR}.${PATCH}
	docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${MAJOR}.${MINOR}
	docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${MAJOR}

publish:
	docker push ${IMAGE_NAME}