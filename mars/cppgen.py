#!/usr/bin/python
from string import Template
class Cppgen(object):
    def __init__(self, name = "0"):
        self.name = name
        #name of the generated test case
    def gen(self,filename,classname,helpfile,pfix,sfix1,sfix2,s2rec):
        self.__fname=filename.split("/")[1]
        self.__cname=classname
        self.__fn2=helpfile.split("/")[1]
        self.__pfix=pfix
        self.__sfix1=sfix1
        self.__sfix2=sfix2
        self.rec=s2rec
    	import os
    	ad=os.getcwd()
    	os.chdir(ad+'/tests')
        os.system('rm -rf *.cpp')
        class_file=open('test_'+self.name+'_gen.cpp','w')
    	os.chdir('..')
        lines=[]
        #template
        tmp_f=open('testskeleton.cpp','r')
        tmp=Template(tmp_f.read())
        #replace
        lines.append(tmp.substitute(
            rec=self.rec,
            filename=self.__fname,
            classname=self.__cname,
            helpfile=self.__fn2,
            PREFIX=self.__pfix,
            SUFFIX1=self.__sfix1,
            SUFFIX2=self.__sfix2))
        # write into file
        class_file.writelines(lines)
        class_file.close()




