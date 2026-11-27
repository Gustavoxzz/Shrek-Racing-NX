#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p build/phase2-objects
for source in generated/shrek-attempt/shrek.c generated/shrek-attempt/shrek_[0-6].c; do
    name=$(basename "$source" .c)
    printf 'Compiling %s\n' "$source"
    gcc -O0 -g1 -fno-strict-aliasing -Ireferences/nakagawa-recomp/src/rt -Ireferences/nakagawa-recomp/src/core -Igenerated/shrek-attempt -c "$source" -o "build/phase2-objects/$name.o"
done
