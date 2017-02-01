python3 scripts/minify.py
git archive --format=zip HEAD > $(cat VERSION.txt).zip
