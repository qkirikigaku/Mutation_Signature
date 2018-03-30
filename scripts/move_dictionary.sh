#!/bin/bash
data_type=$1
cancer_type=$2

target=/home/taro/project/MS_real/code/result/data${data_type}_o400_${cancer_type}
signature_directory=$(find ${target}/figure/* -type d)
figure_directory=${target}/figure
text_directory=${target}

topic_num=${signature_directory##*/}

dic_directory=/home/taro/project/MS_real/code/data/dictionary
dic_file=${dic_directory}/data${data_type}_o400_${cancer_type}

MS_dic=/home/taro/project/Mutation_Signature

if test ${data_type} -eq 2; then
    cp ${dic_file}.txt ${MS_dic}/M2/${cancer_type}/dictionary.txt
fi

if test ${data_type} -eq 7; then
    cp ${dic_file}_indel.txt ${MS_dic}/M3/${cancer_type}/dictionary_indel.txt
fi

if test ${data_type} -eq 9; then
    cp ${dic_file}.txt ${MS_dic}/M4/${cancer_type}/dictionary.txt
    cp ${dic_file}_indel.txt ${MS_dic}/M4/${cancer_type}/dictionary_indel.txt
fi

