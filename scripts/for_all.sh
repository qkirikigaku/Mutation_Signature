#!/bin/bash
script=${1}
types=("breast" "endometrium" "large_intestine" "liver" "lung" "oesophagus" "prostate" "skin" "soft_tissue" "stomach" "upper_aerodigestive_tract" "urinary_tract")

for i in $(seq 1 2); do
    for j in $(seq 0 11); do
        sh ${script} ${i} ${types[j]}
    done
done
for j in $(seq 0 11); do
    sh ${script} 7 ${types[j]}
done
for j in $(seq 0 11); do
    sh ${script} 9 ${types[j]}
done
