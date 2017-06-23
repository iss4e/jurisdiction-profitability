## PARAMETERS ##
param a1;             # tier 1 grid price
param a2;             # tier 2 grid price
param a3;             # tier 3 grid price
param a4;             # tier 4 grid price
param a5;             # tier 5 grid price

param a1s;
param a2s;
param a3s;
param a4s;
param a5s;

param gamma1;         # first threshold
param gamma2;         # second threshold
param gamma3;
param gamma4;
param M;              # months
set months = 1..M;

set winter_months = {1, 2, 3, 4, 5, 10, 11, 12};
set summer_months = {6, 7, 8, 9};

#param m_index {m in months, day in 1..30} = (m-1)*30 + day;

## VARIABLES ##
var pi0 {m in months,y in 1..Y} >= 0;
var pi1 {m in months, y in 1..Y} >= 0;
var pi2 {m in months, y in 1..Y} >= 0;
var pi3 {m in months, y in 1..Y} >= 0;
var pi4 {m in months, y in 1..Y} >= 0;
var month_use {m in months, y in 1..Y};

## OBJECTIVE ##
maximize revenue:
  (sum {y in 1..Y} (sum {t in 1..T}  (p_plus*e[t,y]*T_u)/((1+i)^y) - (sum {m in winter_months} (a1*pi0[m,y] + a2*pi1[m,y] + a3*pi2[m,y] + a4*pi3[m,y] + a5*pi4[m,y])*z[y]) - (sum {m in summer_months} (a1s*pi0[m,y] + a2s*pi1[m,y] + a3s*pi2[m,y] + a4s*pi3[m,y] + a5s*pi4[m,y])*z[y]) - 
    (sum {t in 8640..T} g[t,y]*T_u*a1*z[y]))) - PV*inv_pv - B*inv_b;


## CONSTRAINTS ##
subject to c1 {m in months, y in 1..Y}:
  pi0[m,y] <= gamma1;

subject to c2 {m in months, y in 1..Y}:
  pi1[m,y] <= gamma2;

subject to c3 {m in months, y in 1..Y}:
  pi2[m,y] <= gamma3;

subject to c4 {m in months, y in 1..Y}:
  pi3[m,y] <= gamma4;  

#subject to c5 {m in months, y in 1..Y}:
#  pi0[m,y] <= month_use[m,y];

#subject to c6 {m in months, y in 1..Y}:
#  pi0[m,y] + pi1[m,y] <= month_use[m,y];

#subject to c7 {m in months, y in 1..Y}:
#  pi0[m,y] + pi1[m,y] + pi2[m,y] <= month_use[m,y];

#subject to c8 {m in months, y in 1..Y}:
#  pi0[m,y] + pi1[m,y] + pi2[m,y] + pi3[m,y] <= month_use[m,y];

subject to c9 {m in months, y in 1..Y}:
  pi0[m,y] + pi1[m,y] + pi2[m,y] + pi3[m,y] + pi4[m,y] = month_use[m,y];

subject to month_use_def {m in months, y in 1..Y}:
  month_use[m,y] = sum {t in ((m-1)*30*24+1)..m*30*24} (g[t,y]*T_u);

#subject to g_lim {t in 1..T, y in 1..Y}:
#  g[t,y] <= 200;
