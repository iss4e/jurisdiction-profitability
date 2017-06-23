#!/usr/bin/python

from subprocess import call
import os

maxnum=90

for i in range(maxnum):
    # Load and solar data is expected to be stored in the hourly_data folder.
    # Here, we check if the file with id=i exists, before proceeding.
    fname = "hourly_data/Load_" + str(i) + ".dat"
    if not(os.path.isfile(fname)):
        continue
    
    num_lines = sum(1 for line in open(fname))

    # Create script
    script_file = "scripts/script" + str(i) + "_flatprice.ampl"
    f = open(script_file, 'w')

    # read the file containing the total grid payment with no system
    pns_file = open("results/results_ns_"+str(i), 'r')
    pns = pns_file.read();

    f.write("model model_roi.mod;\n")
    f.write("model objective_flatprice_roi.mod;\n")
    f.write("data hourly_data/PV_ampl.dat;\n")
    f.write("data hourly_data/Load_" + str(i) + ".dat;\n")
    f.write("data data_roi.dat;\n")   
    f.write("data z_germany.dat;\n")           
    f.write("\n")

    f.write("option solver cplex;\n")
    f.write("\n")
    
    f.write("let PV := 10;\n")

    f.write("for {pv_factor in 1..5} {\n")
    f.write("let PV := pv_factor*2;\n");
    f.write("for {b_factor in 0..5} {\n")
    f.write("\tlet B := b_factor;\n")
    f.write("\tlet PNS := " + pns + "*(-1);\n")
    f.write("\tsolve;\n")
    f.write("\tprintf \"%f %f %f\\n\", revenue, B, PV > results/results_" + str(i) + ";\n")
    f.write("}\n")    
    f.write("}\n")    

    f.write("\n")
    f.write("quit;\n")
    f.close()

    # Run script
    cmd= "ampl " + script_file 
    print cmd
    call(cmd, shell=True)
    print "done."
