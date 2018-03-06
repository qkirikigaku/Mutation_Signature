#!/bin/bash
script=${1}
dictionaries=("1" "2" "3" "4")
types=("breast" "endometrium" "large_intestine" "liver" "lung" "oesophagus" "prostate" "skin" "soft_tissue" "stomach" "upper_aerodigestive_tract" "urinary_tract")

for i in $(seq 1 4); do
    for j in $(seq 0 11); do
    python ${script} ${i} ${types[${j}]}
    done
done

