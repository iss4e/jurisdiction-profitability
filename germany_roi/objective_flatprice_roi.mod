param p_minus;             # grid price

## OBJECTIVE ##
maximize revenue:
        (PNS + ((sum {y in 1..Y} ( sum {t in 1..T} ((p_plus*e[t,y]*T_u)/((1+i)^y) - (p_minus*g[t,y]*z[y]*T_u)))) - PV*inv_pv - B*inv_b))/(PV*inv_pv  + B*inv_b);


