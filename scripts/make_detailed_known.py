import os
import sys

def main():
    args=sys.argv
    #args[1] : dictionary_type = 1, args[2] : cancer_type = 'Known'
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
              '<h1>COSMIC Known Signatures (' + dic_name + ', ' + cancer_type + ')</h1>\n')
    out = load_result(out, dic_name, cancer_type)
    out.write('<p>-----------------------------------------------------------------------------------------------------------</p>\n')
    out.write('<li><a href=index.html>Top page</a></li>\n')
    out.write('</body>\n'\
              '</html>\n')
   
def load_result(out, dic_name, cancer_type):

    out.write('<h2>Description</h2>\n')
    out.write('<p>These mutation signatures are COSMIC Known Signatures.</p>\n')
    out.write('<p>All description is derived from <a href=\"http://cancer.sanger.ac.uk/cosmic/signatures\">COSMIC</a></p>\n')

    num_predicted = 0
    for x in os.listdir('/home/taro/project/Mutation_Signature/' + dic_name + '/' + cancer_type + '/'):
        if(x.startswith('predicted_')):
            num_predicted += 1

    COSMIC_INFO = get_COSMIC_INFO()

    for i in range(num_predicted):
        out.write('<h2 id=' + str(i+1) + '_' + cancer_type + '>COSMIC Known Signature ' + str(i+1) + '</h2>\n')
        out.write('<figure>\n')
        fig_path = dic_name + '/' + cancer_type + '/predicted_' + str(i+1) + '.png'
        out.write('<a href=' + fig_path + ' data-lightbox=\"enlarged\">')
        out.write('<img src=' + fig_path + ' width=400></a>\n')
        out.write('<figcaption>Signature ' + str(i+1) + '</figcaption>')
        out.write('</figure>\n')
        out.write(COSMIC_INFO[i])
        out.write('<br><br>\n')
    return out

def get_COSMIC_INFO():
    COSMIC_INFO = []
    lines = open('/home/taro/project/Mutation_Signature/scripts/COSMIC.html', 'r').readlines()
    flag = 0
    INFO = ''
    for line in lines:
        if(line.find('<div><h4>Cancer types:</h4><span>') > -1):
            flag = 1
        if(line.find('<!-- end of signature-') > -1):
            flag = 0
        if(flag == 1):
            INFO += line
        if(flag == 0 and INFO != ''):
            COSMIC_INFO.append(INFO)
            INFO = ''
    return COSMIC_INFO

if __name__ == '__main__':
    main()
