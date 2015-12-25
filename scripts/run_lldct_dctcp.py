import threading
import os
import sys

class SimThread(threading.Thread):
	def __init__(self, cmd, directory_name):
		self.cmd = cmd
		self.directory_name = directory_name
		threading.Thread.__init__(self)

	def run(self):
		#Make directory to save results
		os.system('mkdir ' + self.directory_name)
		os.system(self.cmd)


sim_end = 100000
link_rate = 10
mean_link_delay = 0.0000002
host_delay = 0.000020
queueSize = 240
load_arr = [0.9,0.8,0.7,0.6,0.5]
connections_per_pair = 1
meanFlowSize = 1138*1460
paretoShape = 1.05
flow_cdf = 'CDF_dctcp.tcl'

enableMultiPath = 1
perflowMP = 0

#sourceAlg='DCTCP-Sack'
sourceAlg = 'LLDCT-Sack'
initWindow = 70
ackRatio = 1
slowstartrestart = 'true'
DCTCP_g = 0.0625
min_rto = 0.002
prob_cap_ = 5

switchAlg = 'Priority'
DCTCP_K = 65.0
drop_prio_ = 'true'
prio_scheme_ = 2
deque_prio_ = 'true'
keep_order_ = 'true'
prio_num_arr = [1]
ECN_scheme_ = 2 #Per-port ECN marking
pias_thresh_0 = 46*1460
pias_thresh_1 = 1084*1460
pias_thresh_2 = 1717*1460
pias_thresh_3 = 1943*1460
pias_thresh_4 = 1989*1460
pias_thresh_5 = 1999*1460
pias_thresh_6 = 2001*1460

topology_spt = 16
topology_tors = 9
topology_spines = 4
topology_x = 1

ns_path = '/home/wei/pias/ns-allinone-2.34/ns-2.34/ns'
sim_script = 'spine_empirical.tcl'

threads = []
max_thread_num = 18


for prio_num_ in prio_num_arr:
	for load in load_arr:

		scheme = 'unknown'
		if switchAlg == 'Priority' and prio_num_ > 1 and sourceAlg == 'DCTCP-Sack':
			scheme = 'pias'
		elif switchAlg == 'Priority' and prio_num_ == 1:
			if sourceAlg == 'DCTCP-Sack':
				scheme = 'dctcp'
			elif sourceAlg == 'LLDCT-Sack':
				scheme = 'lldct'

		if scheme == 'unknown':
			print 'Unknown scheme'
			sys.exit(0)

		#Directory name: workload_scheme_load_[load]
		directory_name = 'websearch_%s_%d' % (scheme, int(load*10))
		directory_name = directory_name.lower()
		#Simulation command
		cmd = ns_path+' '+sim_script+' '\
			+str(sim_end)+' '\
			+str(link_rate)+' '\
			+str(mean_link_delay)+' '\
			+str(host_delay)+' '\
			+str(queueSize)+' '\
			+str(load)+' '\
			+str(connections_per_pair)+' '\
			+str(meanFlowSize)+' '\
			+str(paretoShape)+' '\
			+str(flow_cdf)+' '\
			+str(enableMultiPath)+' '\
			+str(perflowMP)+' '\
			+str(sourceAlg)+' '\
			+str(initWindow)+' '\
			+str(ackRatio)+' '\
			+str(slowstartrestart)+' '\
			+str(DCTCP_g)+' '\
			+str(min_rto)+' '\
			+str(prob_cap_)+' '\
			+str(switchAlg)+' '\
			+str(DCTCP_K)+' '\
			+str(drop_prio_)+' '\
			+str(prio_scheme_)+' '\
			+str(deque_prio_)+' '\
			+str(keep_order_)+' '\
			+str(prio_num_)+' '\
			+str(ECN_scheme_)+' '\
			+str(pias_thresh_0)+' '\
			+str(pias_thresh_1)+' '\
			+str(pias_thresh_2)+' '\
			+str(pias_thresh_3)+' '\
			+str(pias_thresh_4)+' '\
			+str(pias_thresh_5)+' '\
			+str(pias_thresh_6)+' '\
			+str(topology_spt)+' '\
			+str(topology_tors)+' '\
			+str(topology_spines)+' '\
			+str(topology_x)+' '\
			+str('./'+directory_name+'/flow.tr')+'  >'\
			+str('./'+directory_name+'/logFile.tr')

		#Start thread to run simulation
		print cmd
		newthread = SimThread(cmd,directory_name)
		threads.append(newthread)

#Thread id
thread_i = 0
#A temporary array to store running threads
tmp_threads = []
#The number of concurrent running threads
concurrent_thread_num = 0

while True:
	#If it is a legal thread and 'tmp_threads' still has capacity
	if thread_i < len(threads) and len(tmp_threads) < max_thread_num:
		tmp_threads.append(threads[thread_i])
		concurrent_thread_num = concurrent_thread_num + 1
		thread_i = thread_i + 1
	#No more thread or 'tmp_threads' does not have any capacity
	#'tmp_threads' is not empty
	elif len(tmp_threads) > 0:
		print 'Start '+str(len(tmp_threads))+' threads\n'
		#Run current threads in 'tmp_threads' right now!
		for t in tmp_threads:
			t.start()
		#Wait for all of them to finish
		for t in tmp_threads:
			t.join()
		#Clear 'tmp_threads'
		del tmp_threads[:]
		#Reset
		concurrent_thread_num = 0
	#'tmp_threads' is empty
	else:
		break
