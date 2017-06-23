# jurisdiction-profitability
AMPL optimization models and scripts

We use python scripts to write and execute AMPL scripts, which then use CPLEX as the optimization solver.

The folders for each jurisdiction contain all the data needed to compute the ROI of a household EXCEPT for the solar and load data traces. Interested users should look up AMPL documentation for an explanation of how to format their data traces properly. The scripts expect hourly data, but can be easily configured to work with different time-slot durations (change the T_u value in the data.dat files, as well as the grid price files if they are time dependent)

The optimization is done as follows (it is the same for each jurisdiction):
1. First, we compute the payment with no system (i.e. B = 0, PV = 0) using the runAMPL....nosystem.py script. It is possible to do this without using an optimization solver, however CPLEX does not take much time to calculate this value either and we found it easy to manage when all the computation is done using the same tools.
2. Next, we compute the ROI using the runAMPL....py script. This script writes and executes AMPL scripts, one for each available load trace. The results are written to a file.
