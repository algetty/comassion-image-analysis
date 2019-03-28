#! /bin/bash

for file in $(ls)
do
  FIRST=$(awk -F- '{$1}' file)
  echo $first
done
