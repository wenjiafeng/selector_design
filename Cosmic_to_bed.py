#!usr/bin/env python                                                                                                                                         
import os
import pandas as pd
from optparse import OptionParser

#cosmicfile = pd.read_csv('/duo4/users/wenjia/selector_design/selector_dsfiles/CosmicMutation_fathmm.csv', sep='\t',header=None)                             
def search_in_cosmic(searchlist):
    #with open('/duo4/users/wenjia/selector_design/selector_dsfiles/searchlist_coad_ha.txt') as l:                                                           
    print("search genes in Cosmic file:\n")
    with open(searchlist) as l:
        searchlist=l.readlines()
        outname=l.name[0:-4]+'_out.txt'
        for i in searchlist:
            i=i.split('\n')
            a=i[0]
            os.system('grep -w '+ a +' CosmicMutation_fathmm.csv | sort | uniq >> '+ outname)

    print("get bed format for gene with fathmm score bigger than 0.98:\n")
    outfile=outname[0:-3]+'bed'
    with open(outfile,'a') as f:

        with open(outname) as o:
            fathmm=o.readlines()
            for j in fathmm:
                item=j.split('\t')
                item[2]='0'+ item[2].split('\n')[0]
                if float(item[2]) >=0.98:
                    info=item[1].split(":")
                    chrome= 'chr'+info[0]
                    end=info[1].split("-")[1]
                    start = str(int(end)-1)
                    #print(chrome + "\t" + start+"\t"+end+"\t"+item[0]+"\n", file=f)                                                                         
                    print >> f, chrome + "\t" + start+"\t"+end+"\t"+item[0]
    os.system("rm "+outname)

    print("change chr23 to chrX for later intersect step:\n")
    os.system("sed -i \"s/chr23/chrX/g\" "+ outfile)

    ##intersection step                                                                                                                                      
    print("get intersected bed file:\n")
    intersectfile=outfile[0:-4]+"_intersect.txt"
    os.system("bedtools intersect -a /duo4/users/wenjia/selector_design/selector_dsfiles/RefSeq_Gencodev17_022314.allexons.bed -b "+outfile+" -wo >> "+inter\
sectfile)
    bedfile=intersectfile[0:-3]+"bed"
    os.system("cut -f 1,2,3,4 "+intersectfile+ " > "+ bedfile)

    ###remove n/a and repeat                                                                                                                                 
    os.system("sed -i -e \'/n\/a/d\' "+ bedfile)
    output="output_"+l.name[0:-4]+".bed"
    os.system("awk \' !x[$0]++\' "+ bedfile +" > "+output)
    ###remove files                                                                                                                                          
    os.system("rm "+outfile)
    os.system("rm "+intersectfile)
    os.system("rm "+bedfile)

def main():
    usage = "usage:%prog [options] arg"
    parser = OptionParser()
    parser.add_option("-f", dest="searchlist", help="provide input file", metavar="FILE")
    (options, args) = parser.parse_args()
    if not options.searchlist:
        parser.error("Provide the filename with -f option.")
    search_in_cosmic(options.searchlist)

if __name__ == "__main__":
    main()

