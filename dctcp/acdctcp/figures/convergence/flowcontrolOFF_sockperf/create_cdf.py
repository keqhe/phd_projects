#blatantly stole and modified from:
# http://www.phacai.com/calculating-cdf-python-code
#
#
# Takes in an array, sorts it (in place), then calculates the CDF
#  Right now just outputs <val> <cumulative %> to stdout 
#
class create_cdf(object):
    
    def __init__(self, src):        
        self.data_array = src
        self.traceLen = len(src)

    #
    # input: outputfile we should write into
    # verbose: whether we should print to stdout
    #
    def cdf(self, outputfile, verbose):
        cur = -1
        prev = -1
        totalPercentage = 0.0
        self.data_array.sort()

        file = open(outputfile, 'w')
        
        for line in self.data_array:
            cur=float(line)
            if cur!=prev:
                if prev>=0:
                    pctg=1.0*count/self.traceLen
                    totalPercentage+=pctg
                    file.write(str(prev)+" "+str(totalPercentage)+"\n")
                    if (verbose):
                        print str(prev)+" "+str(totalPercentage)
                prev=cur
                count=0
            count+=1
        if prev>=0:
            pctg=1.0*count/self.traceLen
            totalPercentage+=pctg
            file.write(str(prev)+" "+str(totalPercentage)+"\n")
            if (verbose):
                print str(prev)+" "+str(totalPercentage)
    

        file.close()
