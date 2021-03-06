#!/usr/bin/python

from subprocess import call
import os

maxnum=90

for i in range(maxnum):
    # Load and solar data is expected to be stored in the hourly_data folder.
    # Here, we check if the file with id=i exists, before proceeding.
    fname = "AMPL_files/Load_" + str(i) + ".dat"
    if not(os.path.isfile(fname)):
        continue
    
    num_lines = sum(1 for line in open(fname))

    # Create script
    script_file = "scripts/script_nosystem_" + str(i) + "_flatprice.ampl"
    f = open(script_file, 'w')

    f.write("model model_nosystem.mod;\n")
    f.write("model objective_flatprice.mod;\n")
    f.write("data pv1_ampl.dat;\n")
    f.write("data AMPL_files/Load_" + str(i) + ".dat;\n")
    f.write("data data_nosystem.dat;\n")   
    f.write("data z_germany.dat;\n")
    f.write("\n")

    f.write("option solver cplex;\n")
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
