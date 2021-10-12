APP="giuseppe7/rose"
VERSION=v`cat build_number`

build:
	@docker build . -t $(APP):$(VERSION) && docker tag $(APP):$(VERSION) $(APP):latest
