#!/usr/bin/env python

import sys
import sqlite3 as lite 
from tar_info import Target
import params as p

def create_log(tar_file):
    try:
        
        target = Target()
        target.from_file(p.tar_dir + '%s' % tar_file)
        con = lite.connect('client.db')
        cur = con.cursor()
        
        with con:
            cur.execute("INSERT INTO Accepted_targets(Timestamp, Name, RA, DEC, FILTER, Number_of_Exposures, Exposure_time) VALUES(datetime(), ?, ?, ?, ?, ?, ?);" ,(target.Name, target.RA, target.Dec, target.Filter, target.No_exp, target.Exp_time))
            print 'Target added to database.'
    
    except Exception as e:
        con.rollback()
        raise e

    finally:
        con.close()
          
        



    
