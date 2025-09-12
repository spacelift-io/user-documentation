.PHONY: run
run:
	docker compose up

.PHONY: lint
lint: markdown-lint oxipng

.PHONY: markdown-lint
markdown-lint:
	docker run -v ${PWD}:/app:ro -w /app --rm ghcr.io/tcort/markdown-link-check:stable --config=markdown-link-check.json .

.PHONY: oxipng
oxipng:
	docker run --rm -v $(pwd):/app -w /app ghcr.io/shssoichiro/oxipng:v9.1.5 --opt=4 --preserve --strip=safe -r /app
