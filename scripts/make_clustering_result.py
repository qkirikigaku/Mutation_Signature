import sys

def main():
    args=sys.argv
    #args[1] : dictionary_type = 1|2|3|4
    dic_name = 'M' + args[1]
    out_file = '/home/taro/project/Mutation_Signature/'\
                + dic_name + '_Clustering.html'
    out = open(out_file, 'w')

    out.write('<!DOCTYPE html>\n'\
              '<html lang=\"en\">\n'\
              '<link rel=\"stylesheet\" type=\"text/css\" href=\"clustering.css\">\n'\
              '<head>\n'\
              '<link href=\"https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/css/lightbox.css\" rel=\"stylesheet\">\n'\
              '<script src=\"https://code.jquery.com/jquery-1.12.4.min.js\" type=\"text/javascript\"></script>\n'\
              '<script src=\"https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.7.1/js/lightbox.min.js\" type=\"text/javascript\"></script>\n'\
              '<title>' + dic_name + '_Clustering</title>\n'\
              '</head>\n'\
              '<body bgcolor=#FFDBC9>\n'\
              '<h1>Clustering Result (' + dic_name + ')</h1>\n')
    out = load_result(out, dic_name)
    out.write('<p>-----------------------------------------------------------------------------------------------------------</p>\n')
    out.write('<li><a href=index.html>Top page</a></li>\n')
    out.write('</body>\n'\
              '</html>\n')
   
def load_result(out, dic_name):
    cluster_figure = dic_name + '/' + dic_name + '_hierarchy_Cosine.png'
    cluster_txt = dic_name + '/' + dic_name + '_clustering.txt'

    out.write('<h2>Hierarchical clustering</h2>\n')
    out.write('<p>This page shows hierarchical clustering result.</p>\n')
    out.write('<p>Reference distance is cosine distance, and\n'\
              'average method is used for linkage clusters.</p>\n')
    out.write('<img src=' + cluster_figure + ' width=1440>\n')

    input_clusters = open(cluster_txt, 'r').readlines()
    num_cluster = len(input_clusters)
    clusters = []
    labels = []
    for i in range(num_cluster):
        clusters.append(get_path(input_clusters[i][:-1], dic_name))
        labels.append(get_label(input_clusters[i][:-1]))

    out.write('<h2>Detected clusters</h2>\n')
    out.write('<p>We regarded signature groups that cosine distances between their members were less than 0.2 as cluster.</p>\n')
    out.write('<p>Then, ' + str(num_cluster) + ' clusters are detected, and they are shown as below.</p>\n')

    for i in range(num_cluster):
        out.write('<h3>Cluster ' + str(i+1) + '</h3>\n')
        for j in range(len(clusters[i])):
            out.write('<figure>\n')
            out.write('<a href=' + clusters[i][j] + ' data-lightbox=\"enlarged\">')
            out.write('<img src=' + clusters[i][j] + ' width=400></a>\n')
            out.write('<figcaption><a href=' + dic_name + '_Detailed_' + labels[i][j][1] + '.html#' + labels[i][j][0] + '_' + labels[i][j][1]
                      + ' target=_blank>' + labels[i][j][0] + ' (' + labels[i][j][1] + ')</a></figcaption>')
            out.write('</figure>\n')

    return out

def get_path(cluster, dic_name):
    clusters = cluster.split(',')
    path_list = []
    for signature in clusters:
        type_start = signature.index('(') + 1
        type_end = signature.index(')')
        cancer_type = signature[type_start:type_end]
        number_end = signature.index(' ')
        signature_number = signature[:number_end]
        path_list.append(dic_name + '/' + cancer_type + '/predicted_' + signature_number + '.png')
    return path_list

def get_label(cluster):
    clusters = cluster.split(',')
    label_list = []
    for signature in clusters:
        type_start = signature.index('(') + 1
        type_end = signature.index(')')
        cancer_type = signature[type_start:type_end]
        number_end = signature.index(' ')
        signature_number = signature[:number_end]
        label_list.append([signature_number, cancer_type])
    return label_list


if __name__ == '__main__':
    main()
