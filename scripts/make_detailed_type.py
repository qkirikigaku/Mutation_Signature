import os
import sys

def main():
    args=sys.argv
    #args[1] : dictionary_type = 1|2|3|4, args[2] : cancer_type = TYPE
    dic_name = 'M' + args[1]
    cancer_type = args[2]
    out_file = '/home/taro/project/Mutation_Signature/'\
                + dic_name + '_Detailed_' + cancer_type + '.html'
    out = open(out_file, 'w')

    out.write('<!DOCTYPE html>\n'\
              '<html lang=\"en\">\n'\
              '<link rel=\"stylesheet\" type=\"text/css\" href=\"clustering.css\">\n'\
              '<head>\n'\
              '<link href=\"https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/css/lightbox.css\" rel=\"stylesheet\"\n>'\
              '<script src=\"https://code.jquery.com/jquery-1.12.4.min.js\" type=\"text/javascript\"></script>\n'\
              '<script src=\"https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/js/lightbox.min.js\" type=\"text/javascript\"></script>\n'\
              '<title>' + dic_name + '_detailed_' + cancer_type + '</title>\n'\
              '</head>\n'\
              '<body bgcolor=#FFDBC9>\n'\
              '<h1>Predicted Signatures (' + dic_name + ', ' + cancer_type + ')</h1>\n')
    out = load_result(out, dic_name, cancer_type)
    out.write('<p>-----------------------------------------------------------------------------------------------------------</p>\n')
    out.write('<li><a href=index.html>Top page</a></li>\n')
    out.write('</body>\n'\
              '</html>\n')
   
def load_result(out, dic_name, cancer_type):

    num_predicted = 0
    for x in os.listdir('/home/taro/project/Mutation_Signature/' + dic_name + '/' + cancer_type + '/'):
        if(x.startswith('predicted_')):
            num_predicted += 1

    out.write('<h2>Predicted Signatures</h2>\n')
    out.write('<p>' + str(num_predicted) + ' signatures are extracted with mutation dictionary ' + dic_name + ' in ' + cancer_type + ' by Variational Bayes inference.</p>\n')
    out.write('<figure>\n')
    fig_path = dic_name + '/' + cancer_type + '/VLB.png'
    out.write('<a href=' + fig_path + ' data-lightbox=\"enlarged\">')
    out.write('<img src=' + fig_path + ' width=700></a>\n')
    out.write('<figcaption>Transition of Variational Lower Bound by the number of signatures<figcaption>\n')
    out.write('</figure>\n')

    out.write('<h2>Description</h2>\n')
    out.write('<p>These mutation signatures are Predicted Signatures experimentally.</p>\n')
    out.write('<ul>\n')
    if(dic_name in ['M1', 'M3']):
        out.write('<li>Signature <i>n</i> : shows signature normally. </li>\n')
        out.write('<li>Matched (Cosine distance = <i>x</i>) : shows the most similar COSMIC Known Signature from Signature <i>n</i>'\
                  ' (defined by Cosine distance, and <i>x</i> shows that value).</li>\n')
    else:
        out.write('<li>Marginalized <i>n</i> : shows Signature <i>n</i> marginalized for detailed mutation context of substitution (for M2 and M4).</li>\n')
        out.write('<li>Matched (Cosine distance = <i>x</i>) : shows the most similar COSMIC Known Signature from Marginalized <i>n</i>'\
                  ' (defined by Cosine distance, and <i>x</i> shows that value).</li>\n')
    if(dic_name in ['M3', 'M4']):
        out.write('<li>Indels : shows the indel component of Signature <i>n</i> with simple context (for M3 and M4).</li>\n')
    if(dic_name in ['M2', 'M4']):
        out.write('<li>In detail : shows the detailed substitution context for M2 and M4.</li>\n')
    out.write('</ul>\n')

    match_list = get_match(dic_name, cancer_type)
    match_cos_list = get_match_cos(dic_name, cancer_type)

    for i in range(num_predicted):
        num = str(i+1)
        out.write('<h3 id=' + num + '_' + cancer_type + '>Signature ' + num + '</h3>\n')
        out.write('<figure>\n')
        fig_path = dic_name + '/' + cancer_type + '/predicted_' + num + '.png'
        out.write('<a href=' + fig_path + ' data-lightbox=\"enlarged\">')
        out.write('<img src=' + fig_path + ' width=400></a>\n')
        if(dic_name in ['M1','M3']):
            out.write('<figcaption>Signature ' + num + '</figcaption>\n')
        else:
            out.write('<figcaption>Marginalized ' + num + '</figcaption>\n')
        out.write('</figure>\n')
        
        matched_num = match_list[i]
        out.write('<figure>\n')
        fig_path = 'M1/Known/predicted_' + matched_num + '.png'
        out.write('<a href=' + fig_path + ' data-lightbox=\"enlarged\">')
        out.write('<img src=' + fig_path + ' width=400></a>\n')
        out.write('<figcaption><a href=M1_Detailed_Known.html#' + matched_num + '_Known target=_brank>Matched (Cosine distance = ' + match_cos_list[i][:6] + ')</a></figcaption>\n')
        out.write('</figure>\n')
        
        if(dic_name in ['M3', 'M4']):
            out.write('<figure>\n')
            fig_path = dic_name + '/' + cancer_type + '/indel_' + num + '.png'
            out.write('<a href=' + fig_path + ' data-lightbox=\"enlarged\">')
            out.write('<img src=' + fig_path + ' width=400></a>\n')
            out.write('<figcaption>Indels</figcaption>\n')
            out.write('</figure>\n')

        if(dic_name in ['M2', 'M4']):
            out.write('<p>In detail</p>\n')
            context = ['CtoA','CtoG','CtoT','TtoA','TtoC','TtoG']
            fixed_context = ['[C&gt;A]','[C&gt;G]','[C&gt;T]','[T&gt;A]','[T&gt;C]','[T&gt;G]']
            for j in range(6):
                out.write('<figure>\n')
                fig_path = dic_name + '/' + cancer_type + '/detail_context_' + num + '_' + context[j] + '.png'
                out.write('<a href=' + fig_path + ' data-lightbox=\"enlarged\">')
                out.write('<img src=' + fig_path + ' width=480></a>\n')
                out.write('<figcaption> Detail context for ' + fixed_context[j] + '</figcaption>\n')
                out.write('</figure>\n')

    return out

def get_match(dic_name, cancer_type):
    lines = open('/home/taro/project/Mutation_Signature/' + dic_name + '/' + cancer_type + '/matching.txt', 'r').readlines()
    match_list = []
    for line in lines:
        num = line[:-1]
        match_list.append(num)
    return match_list

def get_match_cos(dic_name, cancer_type):
    lines = open('/home/taro/project/Mutation_Signature/' + dic_name + '/' + cancer_type + '/minimum_cos.txt', 'r').readlines()
    match_cos_list = []
    for line in lines:
        num = line[:-1]
        match_cos_list.append(num)
    return match_cos_list

if __name__ == '__main__':
    main()
