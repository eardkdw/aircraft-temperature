#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#reads and parses the shared memory written my mds02.c. 
# Relies on presence of mds02.py, generated by:
#   ctypesgen.py -o mds02.py faketime_t.h mds02.h
#with faketime_t.h containing, e.g:
#    typedef int time_t;
# to force a particular type for time_t (it varies with system)

import sysv_ipc
from mds02 import * #supplies Misc, Plane, P_MAX
from ctypes import memmove, addressof

#shared_memory_id=50626617 # integer 


class AircraftTemp():
   TEMP_CONST=38.967854 # from http://www.csgnetwork.com/machonecalc.html
   CELSIUS_OFFSET = 273.15 #offsel vs Kelvin
  
   def __init__(self, shared_memory_id): 
      self.imem = sysv_ipc.attach(shared_memory_id)
      self.misc = Misc()
   
      self.sizeofplane=sizeof(Plane) 
      self.unpack()
   
   #Structure of shared memory is:
   # empty Plane instance, P_MAX Plane instances, Misc
   
   def unpack(self):
      #unpack Misc
      misc_address = self.imem.address + (P_MAX + 1)*self.sizeofplane
      memmove(addressof(self.misc), misc_address, sizeof(Misc))
      
      self.P_MAX_C= self.misc.P_MAX_C
      self.planes = []
   
      #unpack plane (0 is dummy empty record?)
      for i in range (0, self.P_MAX_C):
         self.planes.append(Plane())
         pi = addressof(self.planes[i])
         memmove(pi, self.imem.address + i *self.sizeofplane, self.sizeofplane)
      
      #memstring=imem.read()
      #print memstring.find('MUSIC')
      #print memstring.find('EZY89JU')
   
      #print 'Ident, Latitude, Longitude, Altitude / ft, T / °C'
   def airtemp(self, plane):
      TK = (plane.bds.tas_50/(plane.bds.mach_60*self.TEMP_CONST))**2
      return TK - self.CELSIUS_OFFSET

   def position_temperature(self):
      out = []
      for i in range (0, self.P_MAX_C):
         out.append([self.planes[i].acident, self.planes[i].lat, self.planes[i].lon, self.planes[i].alt, self.airtemp(self.planes[i])]);
      return out
         

with open('mds02.log') as f:
   for line in f:
      if 'SHM_ID=' in line:
         print line
         shm_id = int(line[18:-4])
         at = AircraftTemp(shm_id)
         for ac in at.position_temperature():
            print '%9s, %6.4f, %6.4f, %6.0d, %4.2f' % (ac[0], ac[1], ac[2], ac[3], ac[4])
            

