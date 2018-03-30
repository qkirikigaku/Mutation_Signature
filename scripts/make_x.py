import os
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    args = sys.argv
    # args[1] : dictionary_type = 1|2|3|4, args[2] : cancer_type = TYPE
    dic_name = 'M' + args[1]
    cancer_type = args[2]

    directory = '/home/taro/project/Mutation_Signature/' + dic_name + '/' + cancer_type + '/'

    num_predicted = 0
    for x in os.listdir(directory):
        if(x.startswith('predicted_')):
            num_predicted += 1
    num_predicted = num_predicted

    datas = []

    data_file = directory + 'text_signatures.txt'
    data = open(data_file, 'r')
    datas.append(data)

    if dic_name in ['M2','M4']:
        dic_file = directory + 'dictionary.txt'
        dic = open(dic_file, 'r')
        datas.append(dic)

    if dic_name in ['M3','M4']:
        dic_indel_file = directory + 'dictionary_indel.txt'
        dic_indel = open(dic_indel_file, 'r')
        datas.append(dic_indel)

    num_mutation, dictionary = make_dictionary(dic_name, datas)
    # print('predicted: ' + str(num_predicted))
    # print('mutation: ' + str(num_mutation))
    # print(dictionary)

    proportions = make_proportions(data, num_predicted, num_mutation)
    # print(proportions)

    for i in range(num_predicted):
        detailed_description = open(directory + 'detailed_description_' + str(i+1) + '.txt', 'w')
        detailed_description.write('Detailed Description of ' + dic_name + ' ' + cancer_type + ' predicted signature ' + str(i+1) + '\n\n')
        detailed_description = write_peaks(detailed_description, proportions[i], dictionary, dic_name)
        detailed_description = write_dictionary(detailed_description, dictionary)
        detailed_description = write_proportion(detailed_description, proportions[i])
        detailed_description.close()

    print('complete ' + dic_name + ' - ' + cancer_type + '\n')

def make_proportions(data, num_predicted, num_mutation):
    proportions = np.zeros([num_predicted, num_mutation])
    count = 0
    index = 0
    for data_fragment in data.readlines():
        if count >= 2 and count < 2 + num_predicted:
            data_fragments = data_fragment[:-1].split()
            for i in range(num_mutation):
                proportions[index, i] = float(data_fragments[i])
            index += 1
        count += 1
    return proportions

def make_dictionary(dic_name, datas):
    bases = ['A','C','G','T']
    subs = ['[C>A]','[C>G]','[C>T]','[T>A]','[T>C]','[T>G]']
    dic = []
    if dic_name in ['M1','M3']:
        for i in range(96):
            mutation_tail = bases[i % 4]
            mutation_head = bases[i // 24]
            mutation = mutation_head + subs[i // 4 % 6] + mutation_tail
            dic.append(mutation)
        if dic_name == 'M3':
            dic_indel = datas[1]
            for word in dic_indel.readlines():
                dic.append(word[:-1])
        num_mutation = len(dic)
        return num_mutation, dic
    elif dic_name in ['M2', 'M4']:
        dic_sub = datas[1]
        for word in dic_sub.readlines():
            dic.append(word[:-1])
        if dic_name == 'M4':
            dic_indel = datas[2]
            for word in dic_indel.readlines():
                dic.append(word[:-1])
        num_mutation = len(dic)
        return num_mutation, dic
    else:
        return 0, dic

def write_peaks(detailed_description, proportion, dictionary, dic_name):
    bases = ['A','C','G','T']
    subs = ['[C>A]','[C>G]','[C>T]','[T>A]','[T>C]','[T>G]']
    
    detailed_description.write('Peaks\n\n')
    detailed_description.write('One base masked : \n')
    if dic_name in ['M1', 'M3']:
        masked_dic = []
        masked_value = np.zeros([48])
        for i in range(24):
            mutation_head = 'X'
            mutation_tail = bases[i % 4]
            mutation = mutation_head + subs[i // 4] + mutation_tail
            masked_dic.append(mutation)
        for i in range(24):
            mutation_head = bases[i % 4]
            mutation_tail = 'X'
            mutation = mutation_head + subs[i // 4] + mutation_tail
            masked_dic.append(mutation)
        for i, word in enumerate(dictionary):
            if word.startswith('small') or word.startswith('big'): break
            new_word = 'X' + word[1:]
            index = masked_dic.index(new_word)
            masked_value[index] += proportion[i]
            new_word = word[:6] + 'X'
            index = masked_dic.index(new_word)
            masked_value[index] += proportion[i]
        masked_obj = {}
        for i in range(48):
            masked_obj.update({masked_dic[i]:masked_value[i]})
        count = 0
        for key,value in sorted(masked_obj.items(), key=lambda x: -x[1]):
            if(count == 20): break
            detailed_description.write(str(key) + ' : ' + str(np.round(value, 4)) + ' ')
            if value > 0.3: detailed_description.write('**\n')
            elif value > 0.2: detailed_description.write('*\n')
            else: detailed_description.write('\n')
            count += 1
        detailed_description.write('\n')

    elif dic_name in ['M2', 'M4']:
        masked_dic = []
        masked_value = np.zeros([1536])
        for i in range(1536):
            context = [bases[i // 4 % 4], bases[i // 4 // 4 % 4], bases[i // 4 // 4 // 4 % 4]]
            context.insert(i % 4, 'X')
            mutation = context[0] + context[1] + subs[i // 4 // 4 // 4 // 4] + context[2] + context[3]
            masked_dic.append(mutation)
        for i, word in enumerate(dictionary):
            if(word.startswith('small') or word.startswith('big')): break
            for j in range(4):
                context = [word[0], word[1], word[7], word[8]]
                context[j] = 'X'
                new_word = context[0] + context[1] + word[2:7] + context[2] + context[3]
                index = masked_dic.index(new_word)
                masked_value[index] += proportion[i]
        masked_obj = {}
        for i in range(1536):
            masked_obj.update({masked_dic[i]:masked_value[i]})
        count = 0
        for key,value in sorted(masked_obj.items(), key=lambda x: -x[1]):
            if(count == 20): break
            detailed_description.write(str(key) + ' : ' + str(np.round(value, 4)) + ' ')
            if value > 0.2: detailed_description.write('**\n')
            elif value > 0.15: detailed_description.write('*\n')
            else: detailed_description.write('\n')
            count += 1
        detailed_description.write('\n')

    if dic_name in ['M2', 'M4']:
        detailed_description.write('Two bases masked : \n')
        masked_dic = []
        masked_value = np.zeros([576])
        combination = [[0,1], [0,2], [0,3], [1,2], [1,3], [2,3]]
        for i in range(576):
            context = [bases[i // 6 % 4], bases[i // 6 // 4 % 4]]
            for j in range(2):
                context.insert(combination[i % 6][j], 'X')
            mutation = context[0] + context[1] + subs[i // 6 // 4 // 4] + context[2] + context[3]
            masked_dic.append(mutation)
        for i, word in enumerate(dictionary):
            if(word.startswith('small') or word.startswith('big')):break
            for j in range(6):
                context = [word[0], word[1], word[7], word[8]]
                for k in range(2):
                    context[combination[j][k]] = 'X'
                new_word = context[0] + context[1] + word[2:7] + context[2] + context[3]
                index = masked_dic.index(new_word)
                masked_value[index] += proportion[i]
        masked_obj = {}
        for i in range(576):
            masked_obj.update({masked_dic[i]:masked_value[i]})
        count = 0
        for key, value in sorted(masked_obj.items(), key=lambda x: -x[1]):
            if(count == 20): break
            detailed_description.write(str(key) + ' : ' + str(np.round(value, 4)) + ' ')
            if value > 0.25: detailed_description.write('**\n')
            elif value > 0.2: detailed_description.write('*\n')
            else: detailed_description.write('\n')
            count += 1
        detailed_description.write('\n')

        detailed_description.write('Three bases masked : \n')
        masked_dic = []
        masked_value = np.zeros([96])
        for i in range(96):
            context = [bases[i // 4 % 4]]
            for j in range(4):
                if(i % 4 != j):
                    context.insert(j,'X')
            mutation = context[0] + context[1] + subs[i // 4 // 4] + context[2] + context[3]
            masked_dic.append(mutation)
        for i,word in enumerate(dictionary):
            if(word.startswith('small') or word.startswith('big')): break
            for j in range(4):
                context = [word[0], word[1], word[7], word[8]]
                for k in range(4):
                    if(j != k): context[k] = 'X'
                new_word = context[0] + context[1] + word[2:7] + context[2] + context[3]
                index = masked_dic.index(new_word)
                masked_value[index] += proportion[i]
        masked_obj = {}
        for i in range(96):
            masked_obj.update({masked_dic[i]:masked_value[i]})
        count = 0
        for key, value in sorted(masked_obj.items(), key=lambda x: -x[1]):
            if(count == 20): break
            detailed_description.write(str(key) + ' : ' + str(np.round(value, 4)) + ' ')
            if value > 0.3: detailed_description.write('**\n')
            elif value > 0.25: detailed_description.write('*\n')
            else: detailed_description.write('\n')
            count += 1
        detailed_description.write('\n')

    detailed_description.write('\n')
    return detailed_description

def write_dictionary(detailed_description, dictionary):
    detailed_description.write('Dictionary\n')
    for x in dictionary:
        detailed_description.write(x + '\t')
    detailed_description.write('\n\n')
    return detailed_description

def write_proportion(detailed_description, proportion):
    detailed_description.write('Proportion\n')
    for x in proportion:
        detailed_description.write(str(x) + '\t')
    detailed_description.write('\n\n')
    return detailed_description

if __name__ == '__main__':
    main()
