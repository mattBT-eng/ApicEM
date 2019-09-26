import ApicEM
import csv

#open a log file to log all data
l = open('logScript-1.txt', "w+")


###############
###CREATE THE VLAN POOLS
###############

VLANPools = { 'CCG_PHYS_VLP' :
[
'1621',
'1625',
'1629',
'4002',
'504-507',
'1600',
'1617',
'500',
'3601-3604',
'3618',
'3619'
],
'CCG_VMM_VLP':
['1000-1050',
'1051-1100']
}

for VLP,vlans in VLANPools.items():
    VLP_name = VLP
    allocationMode = 'static'
    l.write('Creating VLP %s' %(VLP_name))
    l.write(str(ApicEM.addVLP(VLP_name, allocationMode))+'\n')
    for vlan in vlans:        
        if '-' in vlan:
            v = vlan.split('-')
            rangeFrom,rangeTo = v[0], v[1]
        else:
            rangeTo = vlan
            rangeFrom = rangeTo
        l.write('adding %s to %s vlan range to VLP %s'%(rangeFrom,rangeTo,VLP_name))
        l.write(str(ApicEM.addVlans2VLP(VLP_name, rangeFrom, rangeTo, allocationMode))+'\n')
        

##############
##CREATE THE PHYSICAL DOMAINS
##############
domains = ['CCG_PHYS_DOM_MAN','CCG_PHYS_DOM_WLV']
VLP_name = 'CCG_PHYS_VLP'
for Phy_name in domains:
    l.write('creating physical-domain %s'%(Phy_name))
    l.write(str(ApicEM.createPHY(Phy_name, VLP_name))+'\n')

##############
##CREATE THE AEP DOMAIN
##############
AEP_name = 'CCG_AEP_PHYS'
l.write(str(ApicEM.createAEP(AEP_name))+'\n')
for Phy_name in domains:
    l.write('attaching AEP %s'%(AEP_name))
    l.write(str(ApicEM.attachAEP(AEP_name, Phy_name))+'\n')


#############
##CREATE THE INT AND SW PROFILES. ASSOCIATE THEM
#############
SwitchProfName = ['SW_PROF_101_UK','SW_PROF_102_UK','SW_PROF_103_UK','SW_PROF_104_UK']
IntProfName = ['INT_PROF_101_UK','INT_PROF_102_UK','INT_PROF_103_UK','INT_PROF_104_UK']
for i in range(len(SwitchProfName)):
    l.write('creating Int prof, Swprof, associating both' + IntProfName[i]+SwitchProfName[i])
    l.write(str(ApicEM.createIntProf(IntProfName[i])))
    l.write(str(ApicEM.createSwitchProf(SwitchProfName[i])))
    l.write(str(ApicEM.addIntProfToSwitchProf(SwitchProfName[i], IntProfName[i])))


###############
###CREATE A POLICY GROUP FOR SINGLE INTERFACES
###############
#cdp and lldp enabled
IntPolGrpName = 'INT_POL_GRP_CDP_LLDP'
l.write(('creating PolGrp for single interfaces'+str(ApicEM.createIntPolGrp(IntPolGrpName, AEP_name, LLDP="lldp_enable", CDP = 'CDP_ENABLE'))))



###############
###CREATE INTERFACE SELECTORS FOR ALL SINGLE INTERFACES AND ASSOCIATE THE POLICY GROUP CREATED ABOVE
###############




with open('singles.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

a = 0
for i in your_list:
    a += 1    
    if a == 1: continue
    SwitchProfName,IntProfName,IntSel,Int,PolGrp = i[0],i[1],i[2],i[3],i[4]
    l.write('adding port to IntProf'+str(ApicEM.AddPortSeltoIntProf(IntProfName,IntSel,Int,PolGrp)))


###############
###CREATE INTERFACE SELECTORS FOR ALL VPCS. CREATE VPC POL GRP FOR EACH VPC
###############



with open('VPCs.csv', 'r') as k:
    reader = csv.reader(k)
    your_list = list(reader)

a = 0
for i in your_list:
    a += 1    
    if a == 1: continue
    SwitchProfName,IntProfName,IntSel,Int,PolGrp = i[0],i[1],i[2],i[3],i[4]
    l.write('adding port to IntProf'+str(ApicEM.AddPortSeltoIntProf(IntProfName,IntSel,Int,PolGrp))+'\n')
    if PolGrp not in ApicEM.GetVPC():
        l.write('creating VPC PolGrp'+str(ApicEM.createVPCPolGrp(PolGrp, AEP_name,LACP = 'default'))+'\n')
    l.write('adding port selector to int prof ' + str(ApicEM.AddPortSeltoIntProf(IntProfName,IntSel,Int,PolGrp))+'\n')
    l.write('adding VPCPolGrp to port selector' + str(ApicEM.addVPCPolGrptoPortSel(IntProfName,IntSel,Int,PolGrp))+'\n')


l.close()
