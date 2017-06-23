#!/usr/bin/python

from subprocess import call
import os

# This script is used to generate and AMPL scripts that get us the grid payments with no system (i.e., B=0, PV=0). There results are written to files.

maxnum=10000

for i in range(maxnum):
    # Load and solar data is expected to be stored in the hourly_data folder.
    # Here, we check if the file with id=i exists, before proceeding.
    fname = "hourly_data/Load_" + str(i) + "_hourly.dat"
    if not(os.path.isfile(fname)):
       continue

    num_lines = sum(1 for line in open(fname))

    # Create script
    script_file = "scripts/script_ns_" + str(i) + "_tierprice" + ".ampl"
    f = open(script_file, 'w')

    f.write("model model_nosystem.mod;\n")
    f.write("model objective_tierprice.mod;\n")
    f.write("data hourly_data/PV_8046_hourly.dat;\n")
    f.write("data hourly_data/Load_" + str(i) + "_hourly.dat;\n")
    f.write("data data_nosystem.dat;\n")   
    f.write("data data_tierprice.dat;\n")   
    f.write("data z_texas_decline.dat;\n")
    f.write("\n")

    f.write("option solver cplex;\n")
    f.write("\n")

    f.write("let T := " + str(num_lines-2) + ";\n")
    f.write("\n")  

    f.write("\tsolve;\n")
    f.write("\tprintf \"%f\\n\", revenue > results_pricedecline/results_ns_" + str(i) + ";\n")

    f.write("\n")
    f.write("quit;\n")
    f.close()

    # Run script
    cmd= "ampl " + script_file 
    print cmd
    call(cmd, shell=True)
    print "done."
