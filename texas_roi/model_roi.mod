## GIVEN ##
param T;                # number of time points in one year
param Y;                # number of years
param S{t in 1..T};             # set of pv input
param L{t in 1..T};             # set of load
param p_minus{t in 1..T};             # set of grid prices
param DoD;              # depth of discharge
param MC;               # maximum charge
param alpha_c;          # charge rate limit
param alpha_d;          # discharge rate limit
param eta_c;            # charge efficiency
param eta_d;            # discharge efficiency
param gamma;            # self discharge fraction
param T_u;              # time unit in hours
param p_plus;           # price for selling to grid
param inv_b;            # cost of battery
param inv_pv;           # cost of PV panels
param i;                # inflation rate
param PV;               # pv panel capacity
param B;                # battery energy capacity
param z{1..Y};          # grid price multiplier
param PNS;              # payment with no system

## VARIABLE ##
var g {1..T, 1..Y} >= 0;              # amount bought from grid
var c {1..T, 1..Y} >= 0;              # amount charged
var f {1..T, 1..Y} >= 0;              # amount direct to load
var d {1..T, 1..Y} >= 0;              # amount discharged
var b {0..T, 1..Y} >= 0;              # state of charge
var e {1..T, 1..Y} >= 0;              # sold to grid

## OBJECTIVE ##
# objective function is added in another file
# maximize revenue

## CONSTRAINTS ##
subject to meet_load {t in 1..T, y in 1..Y} : f[t,y] + d[t,y] = L[t] + e[t,y];
subject to balance {t in 1..T, y in 1..Y} : b[t,y] = (1-gamma)*b[t-1,y] + eta_c*c[t,y]*T_u - (d[t,y]/eta_d)*T_u;
subject to initial_b : b[0,1] = B*DoD;
subject to crossover {y in 2..Y} : b[0,y] = b[T,y-1];
subject to lim2 {t in 1..T, y in 1..Y} : c[t,y] + f[t,y] <= PV*S[t] + g[t,y];
subject to c_rate {t in 1..T, y in 1..Y} : c[t,y] <= B*alpha_c;
subject to d_rate1 {t in 1..T, y in 1..Y} : d[t,y] <= B*alpha_d;
subject to blim1 {t in 1..T, y in 1..Y} : B*DoD <= b[t,y];
subject to blim2 {t in 1..T, y in 1..Y} : b[t,y] <= B*MC;
subject to max_sell {t in 1..T, y in 1..Y} : e[t,y] <= PV*S[t];


