#!/bin/bash
# put.sh <file> <signURL> <accessURL> — upload a frame to OpenArt and verify it landed byte for byte
cd "$(dirname "$0")"
curl -sS -X PUT -H "Content-Type: image/png" --data-binary @"$1" -o /dev/null -w "put %{http_code}\n" "$2"
./get.sh "$3" /tmp/_chk.png >/dev/null && cmp -s /tmp/_chk.png "$1" && echo verified || echo MISMATCH
