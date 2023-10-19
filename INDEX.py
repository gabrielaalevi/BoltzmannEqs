{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fb55b561-7e0d-447a-b866-de8a92fed0d2",
   "metadata": {},
   "outputs": [],
   "source": [
    "import math\n",
    "import numpy as np\n",
    "from scipy.special import zeta, kn"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "a556611f-9b0f-4591-bafc-043fc518b815",
   "metadata": {},
   "outputs": [],
   "source": [
    "#constants\n",
    "m_planck = 2.4 * 10**(18) #reduced planck mass, in GeV"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "fb0aa881-6f24-451e-bee5-06e15cf61dd5",
   "metadata": {},
   "outputs": [],
   "source": [
    "def degrees_of_freedom(T): #temperature in GeV\n",
    "    if T >= 0.3:\n",
    "        g = 100\n",
    "    elif T >= 0.1:\n",
    "        g = 10\n",
    "    elif 0.1 > (T):\n",
    "        g = 3\n",
    "    return g"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "063fdd17-da79-4412-9e0e-1991e8e13fcb",
   "metadata": {},
   "outputs": [],
   "source": [
    "def hubble(T): #T for temperature, g for the relativistic number of degrees of freedom\n",
    "    g = degrees_of_freedom(T)\n",
    "    hubble = ((np.pi**2)/90)**(1/2) * g**(1/2) * T**2 / m_planck #hubble constant, varying with temperature\n",
    "    return hubble"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "9ea252b8-cfd2-4c82-a247-545e94a32118",
   "metadata": {},
   "outputs": [],
   "source": [
    "def entropy(T): #entropy density, varying with temperature T and degrees of freedom g\n",
    "    g = degrees_of_freedom(T)\n",
    "    s = (2/45) * (np.pi**2) * g * T**3\n",
    "    return s"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "08d83534-ff13-4585-b722-18ad75bb792e",
   "metadata": {},
   "outputs": [],
   "source": [
    "def equilibrium_yield(m, T, g,b):\n",
    "    #m represents particle's mass, T is temperature in GeV, g represents, particles degrees of freedom, \n",
    "    #and s represents entropy density. b is a parameter, b=0 indicates a fermion, and b=1 indicates a bóson\n",
    "    if T >= 0.3:\n",
    "        g_SM = 100\n",
    "    elif T >= 0.1:\n",
    "        g_SM = 10\n",
    "    elif 0.1 > (T):\n",
    "        g_SM = 3\n",
    "    s = (2/45) * (np.pi**2) * g_SM * T**3\n",
    "    if (m/T)>10:\n",
    "        Y_eq = (g * (m * T/ (2 * np.pi))**(3/2) * np.exp(-m/T))/s\n",
    "    elif (m/T)>(2/3):\n",
    "        Y_eq = (45 * g * (m/T)**2 * kn(2,(m/T)))/(4 * np.pi**4 * g_SM)\n",
    "    elif (m/T)<=(2/3):\n",
    "        if b == 0:\n",
    "            Y_eq = ((3/4) * (zeta(3)/np.pi**2) * g * (T)**3)/s\n",
    "        if b==1:\n",
    "            Y_eq = ((zeta(3)/np.pi**2) * g * (T)**3)/s\n",
    "    return Y_eq"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "99e3fe5d-9c3f-481d-9547-063fb84a774b",
   "metadata": {},
   "outputs": [],
   "source": [
    "def dsdx(x,m):\n",
    "    g = degrees_of_freedom(m/x)\n",
    "    ds_dx = (-6 * np.pi**2 * g * m**3)/(45 * x**4)\n",
    "    return ds_dx"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
