#!/bin/bash
echo "Cube Status Summary"
echo "==================="
echo
echo "Currently RUNNING:"
squeue -u $USER -o "%i" | grep "_" | sed 's/.*_//' | sort -n | uniq | xargs -I{} echo "  Cube {}"
echo
echo "NOT running and need submission:"
for i in {0..15}; do
  if ! squeue -u $USER -o "%i" | grep -q "_${i}$"; then
    echo "  Cube $i"
  fi
done
