0.python 2.7.16 is used
1.PLY-3.0 is used 
2.cppheaderparser(enclosed in the folder) is used
3.help.h is used to generate objects that are needed by the constructor of cut(class under test)
  these objects's type are not including int, char, char[], double and float, which can be generated automatedly by our tool.
4.if you are willing to run with g++, you should specify the additional lib:
	g++ help.h my_q.h test0gen.cpp -o 1 -lpthread



