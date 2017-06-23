#!/usr/bin/python

from subprocess import call
import os

# This script is used to generate and run AMPL scripts to compute the profitability
# for Austin, Texas. The results are written to files with the corresponding id.

maxnum=10000

for i in range(maxnum):
    # Load and solar data is expected to be stored in the hourly_data folder.
    # Here, we check if the file with id=i exists, before proceeding.
    fname = "hourly_data/Load_" + str(i) + "_hourly.dat"
    if not(os.path.isfile(fname)):
       continue

    num_lines = sum(1 for line in open(fname))

    # Create script
    script_file = "scripts/script" + str(i) + "_tierprice" + ".ampl"
    f = open(script_file, 'w')

    pns_file = open("results_pricedecline/results_ns_"+str(i), 'r')
    pns = pns_file.read();

    f.write("model model_roi.mod;\n")
    f.write("model objective_tierprice_roi.mod;\n")
    f.write("data hourly_data/PV_8046_hourly.dat;\n")
    f.write("data hourly_data/Load_" + str(i) + "_hourly.dat;\n")
    f.write("data data_roi.dat;\n")   
    f.write("data data_tierprice.dat;\n")   
    f.write("data z_texas_decline.dat;\n")
    f.write("\n")

    f.write("option solver cplex;\n")
    f.write("\n")

    f.write("let T := " + str(num_lines-2) + ";\n")
    f.write("let PV := 10;\n")
    f.write("let PNS := " + pns + "*(-1);\n")
    f.write("\n")  

    f.write("for {pv_factor in 1..5} {\n")
    f.write("let PV := pv_factor*2;\n")
    f.write("for {b_factor in 0..5} {\n")
    f.write("\tlet B := b_factor;\n")
    f.write("\tsolve;\n")
    f.write("\tprintf \"%f %f %f\\n\", revenue, B, PV > results_pricedecline/results_" + str(i) + ";\n")
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
