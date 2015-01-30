# make 'mds02' 'mds02pr'
# mbr20110827

ADSBPGR_DIR=adsb-pgr-read-only/trunk
CC=g++
#CFLAG=-g

.PHONY: mds init

all:	mds mds02.py

init: 
	svn checkout http://adsb-pgr.googlecode.com/svn/ adsb-pgr-read-only

mds:		
	if [ ! -d $(ADSBPGR_DIR) ]; then $(MAKE) init; fi
	cd $(ADSBPGR_DIR) && svn update
	$(MAKE) -C $(ADSBPGR_DIR)
	cp $(ADSBPGR_DIR)/mds02 bin/
	cp $(ADSBPGR_DIR)/mds02pr bin/
	cp $(ADSBPGR_DIR)/lookup bin/

mds02.py: $(ADSBPGR_DIR)/mds02.h
	ctypesgen.py -o mds02.py faketime_t.h $(ADSBPGR_DIR)/mds02.h	

clean:
	rm -f bin/mds02 bin/mds02pr bin/lookup
