
## Installation

In order to compute the number density for an specific model, it is necessary to:

 1. Instal MadGraph with MadDM
 2. Copy the files [MadDM/get_taacs.f](./MadDM/get_taacs.f), [MadDM/maddm.f](./MadDM/maddm.f) and [MadDM/makefile](MadDM/makefile)  to ``MG5/PLUGIN/maddm/Templates/src/``.

The above steps can also be done running [installer.sh](./installer.sh)


## Computing thermally averaged cross-secions

To compute the $\langle \sigma v \rangle$ for the necessary processes:

 1. Open MadDM on your command prompt, by running:
 
```
cd MG5_aMC_v3_5_4_maddm/bin
python3 ./maddm.py
```
and input the informations for the model desired.

For this, it is necessary to choose a [FeynRules model](https://feynrules.irmp.ucl.ac.be/ "FeynRules"), from their model database, that best describes the desired model. For more informations on how to run MadDM, please refer to their [user guide](https://arxiv.org/abs/2012.09016 "MadDM user guide"). 
   
By running MadDM with the new files, it will generate two new files in the output directory (MG5 > bin > (model just created) > output), names 'taacs.csv' and 'processes_taacs.csv'. These files contain the data for all the possible annihilations reactions in the model, and their respective cross-sections averaged over the temperature.

In the [Examples directory](./Examples), there are some example models. For each model, we have a 'maddm_model.txt' file, with the exact commands inputed in the MadDM command prompt to generate the model, as well as the 'taacs.csv' and 'processes_taacs.csv' files generated by MadDM.

## Computing Decay Widths

4. Run MadGraph in your command prompt, by running:

```
cd MG5_aMC_v3_5_4_maddm/bin
./mg5_aMC
```

6. Import the same FeynRules model used in the previous section.
7. Create a multiparticle class with all the existing BSM particles in the model (along with their antiparticles, if they exist).

For example, imagine we want to run a model where the BSM particles are a Dirac fermion and a real scalar, using a [FeynRules model for t-channel DM collisions](http://feynrules.irmp.ucl.ac.be/wiki/DMsimpt "Simplified t-channel DM model in FeynRules"). In this model, the Dirac fermion is denoted by 'xd', and the real scalar is denoted by 'xs'. Then, we create a multiparticle class (which we will call 'new') by inputing:

```
new = xd xd~ xs
```

7. Generate a random SM SM > BSM BSM collision.

Using the example mentioned above, we could generate the collision of an up quark and an anti-up quark, generating a Dirac fermion and a Dirac anti-fermion. We do this by entering:

```
generate u u~ > xd xd~
```

8. Output and launch the model, by running;

```
output (modelname)
launch (modelname)
```

9. The first message MadGraph shows concerns which features from MadGraph will be used. We do not need to alter anything in this part. Press enter, you should then get a message asking if you would like to change parameters in the param_card.
10. Change the model parameters to be the same as used in the MadDM model, when concerning mass and couplings.
11. For each BSM particle that can decay in the model, change their decay width to 'auto'.

For our example, if we wanted the Dirac fermion to decay, we would input:

```
set wxd auto
```

where the 'w' before the particle name denotes that we are changing its decay width.

Otherwise, it is possible to insert '1' to alter the param_card by hand, using vim. In this case, it is recommended to take a look in a [vim tutorial](https://linuxconfig.org/vim-tutorial "vim tutorial").

Some models have different notations on how to call each particle. In case there is any confusion about different notations, it is recommended to look at the [PDG code](https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf) for the particle in question, and look at the param_card (by pressing 1) to see the correct denomination for the model. For this, look for the 'MASS BLOCK' in the param_card, and search for the PDG code of the particle in question. The PDG codes are in the beggining of each line, and organized in ascending order. After finding the desired PDG code, look at the end of the line. There will be a blue text, preeceded by a '#' symbol. It will be 'm' + the name of the particle in the model.

For example, the left-handed scalar partner of the bottom quark is called b1 in the Monte Carlo Particle Numbering Scheme, and its PDG is 1000005. Looking at the param_card, we find:
![image](https://github.com/user-attachments/assets/b52e80a0-ee2f-49ea-a226-32ac819f2970)




12. Once you are done changing the model's parameters, press enter and let MadGraph run.

In the [Examples directory](./Examples), there are plenty of example models that can be useful. In each folder, we have a 'maddm_model.txt' file, which also has the exact commands inputed in MadGraph for said model.

## Solving the Boltzmann Equations

1. Download all the files on the main directory, and store them in the same folder.

### Input Parameters

On modelParameters, input all the necessary information. They are:
 1. ``nsteps``: the number of steps the code will use to interpolate the cross-sections over the temperature. The higher nsteps, the better the approximation for the cross-sections, but it will require more time to run the code.

 2. ``T_i`` and ``T_f``: the limiting values of temperature that should be used for the data, in GeV.

 3. ``taacs_path``: the path, in your device, for the 'taacs.csv' file

 4. ``processes_path``: the path, in your device, for the 'processes_taacs.csv' file

 5. ``param_path``: the path, in your device, for the 'param_card' file OBTAINED FROM MADGRAPH (not the one obtained from MadDM. By using the MadDM param_card, the decay reactions will not be computed)

 6. ``pnames``: a matrix with all the BSM particles included in the model. Each line of the matrix should be dedicated for one particle. First, it is necessary to input the label of each particle. It is important to note that only one particle should be labeled 'DM', which is the particle that will be used to compute the values of x (m_DM/T). Next, input the type of the particle, as used in the MadDM model, as a string (e.g. 'xd' for a Dirac fermion, 'ul' for the left-handed scalar partner of the up quark), and then the PDG code of the particle. Lastly, we have a parameter called 'in_equilibrium'. If the particle is initially in thermal equilibrium with the plasma, in_equilibrium must be 1 (as for a freeze-out model). If the particle's number density is virtually zero at T_i, in_equilibrium must be 0 (as for a freeze-in model).

 7. ``debug_version``: boolean that turns on and off the production of a 'debug file'. In it, it is printed the values for each term in the Boltzmann Equation divided by Hubble, separated by reaction, for each value of x computed. We know a reaction cease to alter the number density of a particle when its term in the Boltzmann Equation is comparable to the Hubble rate. Hence, in the debug file, a reaction cease to be relevant when BT/H \approx 1 (BT is the Boltzmann term).

 8. ``name_file``: name that should be used to save the files, as a string.

To run the code from a separated python/jupyter notebook file, it is necessary to use 'from boltzSolver import Y'. To run it directly from the command prompt, it is necessary to run the boltzSolver file, which will automatically run the other necessary files.

## Example

An interesting model for DM genesis is the [Conversion-Driven Freeze-out](https://arxiv.org/abs/1904.00238). To compute the number density for this model, the process is:

1. Open MadDM.
```
cd MG5_aMC_v3_5_4_maddm/bin
python3 ./maddm.py
```
2. Import the [FeynRules model for simplified t-channel DM collisions](http://feynrules.irmp.ucl.ac.be/wiki/DMsimpt "Simplified t-channel DM model in FeynRules"). To recreate the examples given in the [CDFO article](https://arxiv.org/abs/1904.00238), we must use the '3rd' modifier for this FeynRules model. This version of the model has DM only interacting with the third generation of quarks, and their respective scalar partners. More information can be found in the [FeynRules framework article](https://arxiv.org/abs/2001.05024).

```
import model DMSimp_t-S3M_3rd
```
3. Define the DM particle as a Majorana fermion, which is denoted by 'xm' in this FeynRules model.

```
define darkmatter xm
```
4. Add a coannihilator to the process. In this model, the coannihilator is a right-handed scalar partner of the bottom quark, denoted by 'b2'.

```
define coannihilator b2
```

5. Generate relic density.

```
generate relic_density
```

6. Output and launch the model.

```
output (modelname)
launch (modelname)
```

7. Change the model's parameters for the ones given on the CDFO article. In this case, we change the Majorana fermion mass to 500, the b2 scalar mass to 510, the lams3d3x3 coupling to 0.17 (this is the coupling between the scalar mediator, the DM fermion and the bottom quark). All the other couplings are zero. This is achieved by running:

```
set mxm 500
set mys3qu3 510
set lams3d3x3 0.17
set lams3q3x3 0
set lams3u3x3 0
```
We note that the b2 scalar is refered by ys3qu3, which is the denomination used by this model, in contrast with the [Monte Carlo Particle Numbering Scheme](https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf), which uses b2. In case there is any confusion about different notations, it is recommended to look at the [PDG code](https://pdg.lbl.gov/2020/reviews/rpp2020-rev-monte-carlo-numbering.pdf) for the particle in question, and look at the param_card (by pressing 6) to see the correct denomination for the model.

8. Press enter and wait for MadDM to finish running.
9. Open MadGraph:

```
cd MG5_aMC_v3_5_4_maddm/bin
./mg5_aMC
```

10. Import the same model as used for MadDM:

```
import model DMSimp_t-S3M_3rd
```

11. Define a multiparticle class with the new particles:

```
define new = xm b2 b2~
```

12. Generate a random SM + SM > BSM + BSM reaction:

```
generate p p > b2 b2~
```

13. Output and launch the model (because the MadDM and MadGraph models are stored in the same folder, it is necessary to use a different name for each model outputed by the different programs):

```
output (modelname-madgraph)
launch(modelname-madgraph)
```

14. You will receive a message about the different modules of MadGraph available for use. We will not need to change anything in this step. Press enter, and you should receive a message asking if you would like to change the model's parameters.
15. Input the same parameters as used in MadDM. In this phase, it is possible that some particles change their denomination, due to a difference in notation between the two programs. 
```
set mxm 500
set mmys3qu3 510
set lams3d3x3 0.17
set lams3q3x3 0
set lams3u3x3 0
```





