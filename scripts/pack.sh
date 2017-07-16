#!/bin/sh

git archive --format=zip HEAD > "$(cat VERSION.txt).zip"
