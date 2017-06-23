#!/usr/bin/python

from subprocess import call
import os

maxnum=100

fname = "ontario_data/PV.dat"
num_lines = sum(1 for line in open(fname))

for i in range(0,maxnum):
    
    # Create script
    script_file = "scripts/script" + str(i) + ".ampl"
    f = open(script_file, 'w')

    pns_file = open("results/results_ns_"+str(i), 'r')
    pns = pns_file.read();

    f.write("model model_roi.mod;\n")
    f.write("model objective_ToUprice.mod;\n")
    f.write("data ontario_data/PV.dat;\n")
    f.write("data ontario_data/Load_" + str(i) + ".dat;\n")
    f.write("data prices_ontario_USD.dat;\n")
    f.write("data data_roi.dat;\n")   
    f.write("data z_ontario.dat;\n")
    f.write("\n")

    f.write("option solver cplex;\n")
    f.write("\n")
    
    f.write("let T := " + str(num_lines-2) + ";\n")
    f.write("let PV := 10;\n")
    f.write("let PNS := " + pns + "*(-1);\n")
    f.write("\n")  

    f.write("for {pv_factor in 1..5} {\n")
    f.write("let PV := pv_factor*2;\n")
    f.write("if PV > 6 then {let p_plus := 0.235;} else {let p_plus := 0.25;}\n")
    f.write("for {b_factor in 0..5} {\n")
    f.write("\tlet B := b_factor;\n")
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
