# Scalable Abstraction-guided Technique for Incremental Rigorous analysis of round-off Errors

Satire is a first order error analysis tools for obtaining rigorous bounds on 
floating point round-off errors. It works on straight line floating-point programs.


# Dependencies

Satire requires the following softwares to be installed.

* Requirements:
	* python > 3.6
	* sly
	* ply
	* symengine
	* sympy
	* gelpia

## Using

Satire is a python based framework. The main function is available is "src/satern.py"
The "--help" command clarifies all the supporting arguments

#### Example1 (with default options)
  > python3 src/satern.py --std --file p3 src/satern.py --std --file large_benchmarks/reduction/Reduction_1024.txt

 The execution generates a `default.log` containing logging traces of the execution for debugging. The output is
 available in `outfile.txt`.
