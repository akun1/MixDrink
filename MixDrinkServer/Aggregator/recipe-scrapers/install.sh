#!/bin/bash
for i in $(cat brew_leaves)
  do
  brew install "$i"
  done
