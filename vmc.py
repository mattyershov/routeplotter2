# vmcattempt = -0.131+0.0229(x)-.000168(x)^2+.000000499(x)^3-.000000000566(x)^4 # line of best fit, use Google Sheets to find one when you have the actual polar


import rangefinder

def calcvmc(wspd, wangle, bearing):
    hdgrange = (bearing - 45, bearing + 45)
