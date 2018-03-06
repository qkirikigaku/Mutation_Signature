#!/bin/bash
data_type=$1
cancer_type=$2

target=/home/taro/project/MS_real/code/result/data${data_type}_o400_${cancer_type}
signature_directory=$(find ${target}/figure/* -type d)
figure_directory=${target}/figure
text_directory=${target}

topic_num=${signature_directory##*/}

if test ${topic_num} -le 9; then
    text_file=result_k0${topic_num}.txt
else
    text_file=result_k${topic_num}.txt
fi

if test ${data_type} -le 2; then
    target_directory=/home/taro/project/Mutation_Signature/M${data_type}/${cancer_type}
fi
if test ${data_type} -eq 7; then
    target_directory=/home/taro/project/Mutation_Signature/M3/${cancer_type}
fi
if test ${data_type} -eq 9; then
    target_directory=/home/taro/project/Mutation_Signature/M4/${cancer_type}
fi

cp ${text_directory}/${text_file} ${target_directory}/text_signatures.txt

cp ${figure_directory}/ELBO_a.png ${target_directory}/VLB.png

cp ${figure_directory}/matching.txt ${target_directory}/matching.txt

cp ${figure_directory}/minimum_cos.txt ${target_directory}/minimum_cos.txt

cp ${figure_directory}/not_match_predicted.txt ${target_directory}/not_match_predicted.txt

if test ${data_type} -eq 7 -o ${data_type} -eq 9; then
    for i in $(seq 1 ${topic_num}); do
        cp ${signature_directory}/indel_${i}.png ${target_directory}
    done
fi

for i in $(seq 1 ${topic_num}); do
    cp ${signature_directory}/predicted_${i}.png ${target_directory}
done

if test ${data_type} -eq 2; then
    for i in $(seq 1 ${topic_num}); do
        cp ${signature_directory}/detail_context_${i}_CtoA.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_CtoG.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_CtoT.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_TtoA.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_TtoC.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_TtoG.png ${target_directory}
    done
fi
if test ${data_type} -eq 9; then
    for i in $(seq 1 ${topic_num}); do
        cp ${signature_directory}/detail_context_${i}_CtoA.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_CtoG.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_CtoT.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_TtoA.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_TtoC.png ${target_directory}
        cp ${signature_directory}/detail_context_${i}_TtoG.png ${target_directory}
    done
fi
