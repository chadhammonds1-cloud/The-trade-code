#!/bin/bash
# get.sh <cdn url> <out file>  — fetch an OpenArt CDN file via Google Storage
u="${1/https:\/\/cdn.openart.ai\//https://storage.googleapis.com/cdn.openart.ai/}"
curl -sS -o "$2" -w "%{http_code} %{size_download}\n" "$u"
