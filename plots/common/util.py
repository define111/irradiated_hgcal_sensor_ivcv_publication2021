from math import *

def TemperatureScaling(temp, Tref):		
	k_b = 8.6173303*10**(-5) #eV/Kelvin
	E_gab = 1.21	#eV
	T = temp+273.15
	Tref += 273.15

	return ((Tref/T)**2 * exp(E_gab/2. * (1/k_b)*(1./T- 1./Tref))).real

def scale_graph(gr, scale=1.):
    for i in range(gr.GetN()):
        gr.GetY()[i] *= scale
        gr.GetEY()[i] *= scale

def yshift_graph(gr, yshift=0.):
	for i in range(gr.GetN()):
		gr.GetY()[i] += yshift

        