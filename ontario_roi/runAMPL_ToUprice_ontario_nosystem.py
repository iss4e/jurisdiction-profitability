#!/usr/bin/python

from subprocess import call
import os

maxnum=100

fname = "ontario_data/PV.dat"
num_lines = sum(1 for line in open(fname))

for i in range(0,maxnum):
    
    # Create script
    script_file = "scripts/script_nosystem_" + str(i) + ".ampl"
    f = open(script_file, 'w')

    f.write("model model_nosystem.mod;\n")
    f.write("model objective_ToUprice_ns.mod;\n")
    f.write("data ontario_data/PV.dat;\n")
    f.write("data ontario_data/Load_" + str(i) + ".dat;\n")
    f.write("data prices_ontario_USD.dat;\n")
    f.write("data data_nosystem.dat;\n")   
    f.write("data z_ontario.dat;\n")
    f.write("\n")

    f.write("option solver cplex;\n")
    f.write("\n")
    
    f.write("let T := " + str(num_lines-2) + ";\n")
    f.write("\n")  

    f.write("\tsolve;\n")
    f.write("\tprintf \"%f\\n\", revenue > results/results_ns_" + str(i) + ";\n")

    f.write("\n")
    f.write("quit;\n")
    f.close()

    # Run script
    cmd= "ampl " + script_file 
    print cmd
    call(cmd, shell=True)
    print "done."
