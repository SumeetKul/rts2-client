import numpy as n
class Target:
	
	#Defining variables and setting define values.
	def __init__(self):
		self.Name     = 'Trigger_00'
		self.RA       = 0.0
		self.Dec      = 0.0
		self.Filter   = None
		self.No_exp   = 1
		self.Exp_time = 15
		
	#Method to readfrom 
	def from_file(self,path):
		t_file = n.loadtxt(path,str)
		self.Name     = t_file[0]
		self.RA       = t_file[1]
		self.Dec      = t_file[2]
		self.Filter   = t_file[3]
		self.No_exp   = int(t_file[4])
		self.Exp_time = int(t_file[5])
