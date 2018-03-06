#!/bin/bash

for i in $(seq 1 4); do
    cp /home/taro/project/MS_real/code/result/general/M${i}_hierarchy_Cosine.png /home/taro/project/Mutation_Signature/M${i}
    cp /home/taro/project/MS_real/code/ref/M${i}_clustering.txt /home/taro/project/Mutation_Signature/M${i}
done
