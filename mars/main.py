#!/usr/bin/python
import sys
import os
from cppgen import Cppgen as cgen
from tasks import instCutTask
from tasks import sfixgen, mtype
import argparse

class Tester(object):
    def __init__(self, args):
        # the class file address
        self.fn1 = args.CUT_filename
        # the class name 
        self.cut = args.CUT_classname
        # the help.h file address
        self.fn2 = args.AS_filename
        # the assistant classes
        self.hcls = args.AS_classnames.split(",")
        # is the generated testcase needs to be built
        self.build = args.if_build
        # the output testcase name
        self.name = args.name
        # the chosen prefix label
        self.pfixlabel = args.prefix_label
        # the chosen suffix keys
        self.sfixlabels1 = [int(x) for x in args.suffix_labels1.split(",")]
        self.sfixlabels2 = [int(x) for x in args.suffix_labels2.split(",")]     
        # initialize some essentials, no need to modify these
        # pair: prefix: suffix generator. suffixed should be generated based on the prefix
        self.p2sgen = {}
                    
    def generate_one(self, ):
        # get predix 
    	prefix=self.getPrefix()	
        # get the generator of suffix corresponding to this prefix
    	sfixgen=self.p2sgen.get(prefix)
        # get suffix with input labels
    	sfix1=sfixgen.nextsfix_label(self.sfixlabels1)
    	sfix2=sfixgen.nextsfix_label(self.sfixlabels2)
        # output the testcase cpp file
    	singlegen=cgen(self.name)
    	singlegen.gen(self.fn1, self.cut, self.fn2, prefix.tos(), sfix1.tos(), sfix2.tos(), sfix2.rectos())  
        # use g++ to compile the cpp file and get the executive file with the given name
        if self.build == True:
            self.mybuild_one()
             
    def show_suffix_method_dict(self, ):
        # show the keys to the methods for suffixes
        sorted_methods_list =  mtype(self.fn1, self.cut, self.fn2, self.hcls).cutmethod()
        ret = {}
        for i, method in enumerate(sorted_methods_list):
            print ("Key ", i)
            print (method.mprint())
            ret[i] = method
        return ret

    def getPrefix(self, ):
        # get the prefix, by default we choose the simplest one
        itask=instCutTask(self.fn1,self.cut,self.fn2,self.hcls)
        # get the chosen prefix
        npfix=itask.cptseqc(self.pfixlabel)
        # store the last return value of prefix, usually the shared variable
        npfix.fixcutv()
        # pair: prefix: suffix generator. suffixed should be generated based on the prefix
        self.p2sgen[npfix]=sfixgen(npfix,self.fn1,self.cut,self.fn2,self.hcls)
        # return the prefix
        return npfix
    
    def mybuild_one(self, ):
        # go to the location of tests folder
    	os.system('pwd')
    	ad=os.getcwd()
    	os.chdir(ad+'/tests')
    	ad1=os.getcwd()
    	files=os.listdir(ad1)
    	testcase  = None
        # find the testcase generated this time
    	for f in files:
    	    if '.cpp' in f and self.name in f:
                testcase = f   	
        # use g++ to complie
		gpp = 'g++ '+testcase+' -o ../myrun/'+testcase.split(".cpp")[0]+' -pthread'
        print (gpp)
        os.system(gpp)
		
if __name__ == "__main__":
    # locate the path to where Mars is
    if not os.path.dirname(sys.argv[0])=='':
	    os.chdir(os.path.dirname(sys.argv[0]))
    # set the input parameters
    parser = argparse.ArgumentParser(description = "Input Parameters:")
    parser.add_argument("--CUT_filename", default = 'tests/my_q.h', type = str, 
                        help = "the path and filename of the class under test")
    parser.add_argument("--CUT_classname", default = 'Queue', type = str,
                        help = "the name of the class under test")
    parser.add_argument("--AS_filename", default = 'tests/help.h', type = str,
                        help = "the path and filename of the assistant class")
    parser.add_argument("--AS_classnames", default = 'as1,ass1', type = str,
                        help = "the name of the assistant class")
    parser.add_argument("--if_build", default = True, type = bool,
                        help = "whether to use g++ to build the generated test case?")
    parser.add_argument("--name", default = "try", type = str,
                        help = "the name of the generated test case")
    parser.add_argument("--prefix_label", default = 0, type = int,
                        help = "which prefix to generate")
    parser.add_argument("--suffix_labels1", default = "0,1,2,3", type = str,
                        help = "a list controling which method to generate in the suffix")
    parser.add_argument("--suffix_labels2", default = "1,0,1,0", type = str,
                        help = "a list controling which method to generate in the suffix")
    parser.add_argument("--show_dict", default = True, type = bool,
                        help = "whether to show the key-method pairs available for suffixes")
    args = parser.parse_args()
    print (args)
    a=Tester(args)
    if args.show_dict:
        a.show_suffix_method_dict()
    else:
        a.generate_one()
    


