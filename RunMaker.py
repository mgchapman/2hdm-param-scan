import os
import imp

jobDir = '/home/mc2r15/data/ParameterScanJobs/' #Where to store jobs for qsub
jobBase = '2hdm_tII_job' #name of job files

runDir = '/scratch/mc2r15/MadgraphInput/' #Where to store madgraph scripts to be run on job
runBase = '2hdm_tII_run' #name of script files

outputDir = '/scratch/mc2r15/ParameterScanOutput/' #Where to put output directories and files (lots of files!)
paramDir = '/home/mc2r15/data/ParameterCards/' #Where to find parameter cards
nJobs = 5 #number of jobs
lines = 5 #number of input lines per job
nEvents = 10000 #number of events per run

#each process must have a corresponding if statement in the loop
processes = ['tIIcardtest_'] 


for prefix in processes:

	at = 1
	inputLine = 1

	for x in range(0,nJobs):

		#make job files
		job = open(jobDir + prefix + jobBase  + str(at), 'w')
		job.write('cd '+outputDir+' \n')
		job.write('$HOME/december/MG5_aMC_v2_5_2/bin/mg5_aMC /scratch/mc2r15/MadgraphInput/'+prefix+'2hdm_tII_run' +str(at))
		job.close()

		#make script files
		run = open(runDir + prefix + runBase + str(at), 'w')

		#if statement contains model imports, process generation, everything up to 'output'
	   	if(prefix == 'ggZh_'):
			run.write('import 2HDMtII_NLO \n')
			run.write('generate g g > z h1 [noborn=QCD] \n')
		elif(prefix == 'qqZh_'):
			run.write('define q = t b c s t~ b~ c~ s~ \n')
			run.write('generate q q > z h1 \n')
	   	elif(prefix == 'tIIcardtest_'):
			run.write('import 2HDMtII_NLO \n')
			run.write('generate g g > z h1 [noborn=QCD] \n')

		else:
			print('Process ' + prefix + ' not defined!')
			os.remove(runDir + prefix + runBase + str(at))
			os.remove(jobDir + prefix + jobBase + str(at))
			quit()

		run.write('output ' + prefix + 'parameterscan' + str(at) + '\n')


		#launches for each input line
		for y in range(0, lines):
			#switches in the parameter card for the next launch
			run.write('shell cp '+paramDir+prefix+'ParameterScanInputs'+str(inputLine)+'.dat '+outputDir+prefix+'parameterscan'+str(at)+'/Cards/param_card.dat \n')
			run.write('launch \n0 \n0 \n')

			inputLine += 1
			
		run.write('launch -i \n')
		run.write('print_results --path=./cross_sections/'+prefix+'cross_section_'+str(at)+'.txt --format=short \n')		

		run.close()

		at += 1

print('Generated '+str(nJobs*len(processes))+' jobs with '+str(nJobs*lines*len(processes))+' total parameter points')
