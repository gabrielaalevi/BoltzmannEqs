#!/usr/bin/env python3

# 1) Run MadGraph using the options set in the input file 
# (the proc_card.dat, parameter_card.dat and run_card.dat...).

from __future__ import print_function
import sys,os,glob
from tools.configParserWrapper import ConfigParserExt
from tools.logger import logger,setLogLevel
import subprocess
import multiprocessing
import tempfile
import time,datetime


def runMadDM(parser):
    """
    Run MadDM to compute widths and relevant collision cross-sections.
    
    :param parser: Dictionary with parser sections.
    
    :return: True if successful. Otherwise False.
    """
        
    #Get run folder:    
    outputFolder = os.path.abspath(parser['Options']['outputFolder'])
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)    
    
    modelDir = os.path.abspath(parser['Model']['modelDir'])
    if not os.path.isdir(modelDir):
        # Check for model restriction in the name
        mDir = modelDir.rsplit('-',1)[0]
        if not os.path.isdir(mDir):
            logger.error(f'Model folder {modelDir} (or {mDir}) not found')
            return False

    dm = parser['Model']['darkmatter']
    bsmList = parser['Model']['bsmParticles'].split(',')
    # Make sure the dmPDG does not appear twice
    bsmList = [p for p in bsmList[:] if p != dm]

    #Generate commands file:       
    commandsFile,cFilePath = tempfile.mkstemp(suffix='.txt', prefix='maddm_commands_', dir=outputFolder)    
    os.close(commandsFile)
    commandsFileF = open(cFilePath,'w')
    commandsFileF.write(f'import model {modelDir}\n')
    commandsFileF.write(f'define darkmatter {dm}\n')
    for p in bsmList:
        commandsFileF.write(f'define coannihilator {p}\n')
    commandsFileF.write('generate relic_density\n')
    commandsFileF.write(f'output {outputFolder}\n')
    commandsFileF.write('launch\n')
    comms = parser["SetParameters"]
    #Set model parameters
    for key,val in comms.items():
        commandsFileF.write(f'set {key} {val}\n')
    
    
    if 'computeWidths' in parser['Model']:
        pList = parser['Model']['computeWidths'].split(',')
        pStr = ' '.join(pList)
        commandsFileF.write(f'compute_widths {pStr}\n')
        commandsFileF.write('done\n')
        commandsFileF.close()
        mg5Folder = parser['Options']['MadGraphPath']
        mg5Folder = os.path.abspath(mg5Folder)        
        if not os.path.isfile(os.path.join(mg5Folder,'bin','maddm.py')):
            logger.error(f'Executable maddm.py not found in {mg5Folder}')
            return False
        # Comput widths
        with open(cFilePath, 'r') as f: 
            logger.debug(f'Running MadDM with commands:\n {f.read()} \n')
        run = subprocess.Popen(f'./bin/maddm.py -f {cFilePath}',shell=True,
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    cwd=mg5Folder)
        
        
         
    output,errorMsg = run.communicate()
    logger.debug(f'MadDM process error:\n {errorMsg.decode("utf-8")} \n')
    logger.debug(f'MadDM process output:\n {output.decode("utf-8")} \n')
    logger.info("Finished MadDM run")

    os.remove(cFilePath)
        
    return True


def main(parfile,verbose):
   
    level = verbose
    setLogLevel(level)    

    parser = ConfigParserExt(inline_comment_prefixes="#")   
    ret = parser.read(parfile)
    if ret == []:
        logger.error( "No such file or directory: '%s'" % args.parfile)
        sys.exit()
            
    #Get a list of parsers (in case loops have been defined)    
    parserList = parser.expandLoops()

    # Start multiprocessing pool
    ncpus = -1
    if parser.has_option("options","ncpu"):
        ncpus = int(parser.get("options","ncpu"))
    if ncpus  < 0:
        ncpus =  multiprocessing.cpu_count()
    ncpus = min(ncpus,len(parserList))
    pool = multiprocessing.Pool(processes=ncpus)
    if ncpus > 1:
        logger.info('Running %i jobs in parallel with %i processes' %(len(parserList),ncpus))
    else:
        logger.info('Running %i jobs in series with a single process' %(len(parserList)))

    now = datetime.datetime.now()
    children = []
    for irun,newParser in enumerate(parserList):
        # Create temporary folder names if running in parallel
        parserDict = newParser.toDict(raw=False)
        logger.debug('submitting with pars:\n %s \n' %parserDict)
        p = pool.apply_async(runMadDM, args=(parserDict,),)
        children.append(p)

#     Wait for jobs to finish:
    output = [p.get() for p in children]
    logger.info("Finished all runs (%i) at %s" %(len(parserList),now.strftime("%Y-%m-%d %H:%M")))

    return output
    


if __name__ == "__main__":
    
    import argparse    
    ap = argparse.ArgumentParser( description=
            "Run a (serial) MadGraph scan for the parameters defined in the parameters file." )
    ap.add_argument('-p', '--parfile', default='input_parameters.ini',
            help='path to the parameters file [input_parameters.ini].')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is info')



    t0 = time.time()

    args = ap.parse_args()
    output = main(args.parfile,args.verbose)
            
    print("\n\nDone in %3.2f min" %((time.time()-t0)/60.))
