param p_minus{t in 1..T};             # set of grid prices

## OBJECTIVE ##
maximize revenue:
        (PNS + (sum {y in 1..Y} ( sum {t in 1..T} ((p_plus*e[t,y]*T_u)/((1+i)^y) - (p_minus[t]*z[y]*g[t,y]*T_u)))) - PV*inv_pv - B*inv_b)/(PV*inv_pv + B*inv_b);
