###################################################################################################################################
#******************Please Update the IP address, username and password for the APIC you want to access below***********************
#**********************************************************************************************************************************
#Contact: abrosahil@gmail.com for any issues.
#The following program contains the backbone functions to execute automation scripts.
#The functions described below form the NorthBound API to the APIC.
#List of functions with corresponding arguments:
#
#	getCookie(url,username,password)				fetches authentication into fabric
#	GetTennantList()								fetches list of all tenants
#	GetAPList(tenant_name)							fetches list of all APs for given tenant
#	GetBDList(tenant_name)							fetches list of all BDs for given tenant
#	GetvrfList(tenant_name)							fetches list of all VRFs for given tenant
#	GetEPGList(tenant_name, apProfile)				fetches list of all EPGs for given tenant and AP
#	GetEPGBDList(tenant_name, apProfile, BDname)	fetches list of all EPGs using a given BD
#	GetBD4EPG(tenant_name, apProfile, EPGname)		fetches the BD for given EPG
#	GetStaticPortsonEPGs(tenant_name, apProfile,EPGname)	RETURNS A LIST -> [pod, leaf, port, vlan(encap)]
#	GetBD4VRF(tenant_name, vrf)						fetches the BD for given VF
#	GetPhy4EPG(tenant_name, apProfile, EPGname)		fetches Physical Domains for given EPGs
#	GetVMMDomainsinEPGs("tenant01","AP1","EPG1")	fetches VMM Domains for given EPGs
#	GetContractList4EPGs(tenant_name,apProfile,EPGname) returns two lists: Consumed Contracts and Provided Contracts
#	GetContractList(tenant_name)					Returns a list of contracts present under Tenant
#	AddSubnetToBD(tenant_name, BDname, subnet,scope)Adds a subnet under tenant BD. PLEASE GIVE SCOPE. Can be "shared" or "private". In the context of VRFs
#	AddSubnetToEPG(tenant_name, apProfile, EPGname, subnet, scope) 
#	AddTennant(tenant_name)							Creates a tenant, arg req. name of tenant
#	AddVRF2Tenant(tenant_name, vrf)					Creates a vrf under a tenant, networking tab
#	AddBD(BDname, tenant_name) 						Creates a bridge domain
#	AssociateVRFToBD(tenant_name, BDname, vrf)		ASSOCIates a vrf to a bd
#	AddEPG(tenant_name, apProfile, BDname, EPGname) Creates EPG, given req. arguments
#	AddAP(tenant_name, apProfile)					Creates an application profile, specify tenant and a name for AP in argument
#	createContractandAssociate(apicIP,tenant_name,apProfile,provEPG,conEPG,contract_name) Creates and associates contracts to EPGs [NOT L3Out]
#	AssociateEPGasProvider(tenant_name,apProfile,EPG,contract_name) Associate a contract to provider EPG 
#	AssociateEPGasConsumer(tenant_name,apProfile,EPG,contract_name)	Associate a contract to consumer EPG 
#	DeleteEPGasConsumer(tenant_name,apProfile,EPG,contract_name)	DE-Associate a contract to provider EPG 
#	DeleteEPGasProvider(tenant_name,apProfile,EPG,contract_name)	DE-Associate a contract to consumer EPG 
#	ConsumeExternalContract(tenant_name,apProfile,EPG,contract_name)	Consume external contracts (inter-tenant)
#	AssociatePhyDom2EPG(tenant_name, apProfile, EPGname, PHY)
#	AssociateVMDom2EPG(tenant, AP, EPG, VM)
#	AssociateStaticPort2EPG(tenant_name, apProfile, EPGname, Vlan, pod,leafpath,port)
#	AssociateVPCPort2EPG(tenant_name, apProfile, EPGname, Vlan, pod,leafpath,port)	Associate VPC port to EPG
#	addVLP(VLP_name, rangeFrom, rangeTo, allocationMode) Creates a VLAN Pool that can be associated later
#	attachAEP(AEP_name, Phy_name)					Creates and attaches Attachable Entity Profile to specified physical domain
#	createPHY(Phy_name, VLP_name)					creates PhysicalDomain and associates with specified VLP name
#	DelEPG(tenant_name, apProfile, EPGname)			Deletes EPG
#################################################################################################################################
import re
import requests
import json

#Credentials to access APIC and ip address of the APIC.
apicIP = "XXXX"
username = "XXXX"
password = "XXXX"


################################################################################################################################################
#Delete leaf access port policy
def delLeafaccport(policy_name):
	url2= "https://%s/api/node/mo/uni/infra/funcprof/accportgrp-%s.json"%(apicIP,policy_name)
	payload = '{"infraAccPortGrp":{"attributes":{"dn":"uni/infra/funcprof/accportgrp-%s","status":"deleted"},"children":[]}}'%(policy_name)
	response2 = requests.request("POST" ,url2, data=payload,headers=headers,verify=False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Delete PC/VPC group policy
def delPCpol(policy_name):
	url2= "https://%s/api/node/mo/uni/infra/funcprof/accbundle-%s.json"%(apicIP,policy_name)
	payload = '{"infraAccBndlGrp":{"attributes":{"dn":"uni/infra/funcprof/accbundle-%s","status":"deleted"},"children":[]}}'%(policy_name)
	response2 = requests.request("POST" ,url2, data=payload,headers=headers,verify=False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function that Deassociates VPC. Requires AP, EPG,pod, leaf and VPC 
def DeAssociateVPC(tenant_name, apProfile,EPGname,pod,leaf,VPC):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s/rspathAtt-[topology/pod-%s/protpaths-%s/pathep-[%s]].json"%(apicIP,tenant_name,apProfile,EPGname,pod,leaf,VPC)
	payload='{"fvRsPathAtt":{"attributes":{"dn":"uni/tn-%s/ap-%s/epg-%s/rspathAtt-[topology/pod-%s/protpaths-%s/pathep-[%s]]","status":"deleted"},"children":[]}}'%(tenant_name,apProfile,EPGname,pod,leaf,VPC)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################








################################################################################################################################################
#Authentication Function: returns headers with authentication cookie inside. Only valid for a few minutes.
def refreshAuth():

	url = "https://%s/api/mo/aaaLogin.json"%(apicIP)
	payload = "{\n\t\"aaaUser\": {\n\t\t\"attributes\": {\n\t\t\t\"name\" : \"%s\",\n\t\t\t\"pwd\": \"%s\"\n\t\t}\n\t}\n}" %(username,password)

	headers2 = {
	    'Content-Type': "application/json",
	    'Cache-Control': "no-cache",
	    }
	response = requests.request("POST", url, data=payload, headers=headers2, verify=False)
	presponse = json.loads(response.text)
	ApicCookie = [presponse['imdata']][0][0]['aaaLogin']['attributes']['token']
	#Common header to be used for all functions
	global headers
	headers = {
		'Content-Type': "application/json",
		'Accept': "application/jsons",
		'cookie': "APIC-cookie=%s" %(ApicCookie),
		'Cache-Control': "no-cache",
			}
	return headers
################################################################################################################################################
#refreshAuth(apicIP,username,password)
refreshAuth()
#print(headers)

################################################################################################################################################
def GetPortsonEPGs(tenant_name, apProfile,EPGname):
    url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children&target-subtree-class=fvRsPathAtt"%(apicIP, tenant_name, apProfile,EPGname)
    response2 = requests.request("GET", url2, headers=headers, verify = False)
    StaticPortsListJson = json.loads(response2.text)
    alist = []
    for i in range(len(StaticPortsListJson["imdata"])):
        path = re.split('/', re.search('\[(.*)\]',StaticPortsListJson["imdata"][i]["fvRsPathAtt"]["attributes"]["dn"]).group(1))
        vlan = StaticPortsListJson["imdata"][i]["fvRsPathAtt"]["attributes"]["encap"]
        try:
            a = re.sub("]", "", path[3]).partition('[')[2]
            if 'eth' in a:                                                              
                a = re.split(']',path[4])[0]
                alist.append(([path[1].partition("-")[2],path[2].partition("-")[2],a, vlan.partition("-")[2]]))
            else:
                alist.append(([path[1].partition("-")[2],path[2].partition("-")[2],a, vlan.partition("-")[2]]))
        except:
            pass
                                #print(path[2].partition("-")[2],re.sub("]", "", path[3]))
    return alist#, StaticPortsListJson4
################################################################################################################################################

################################################################################################################################################
#Function fetches list of tenants available within APIC reach on the Fabric
def GetTenant(tenant):
	#https://11.11.11.161/api/node/mo/uni/tn-TEST_TNT_TEST-01.json
	url2 = "https://11.11.11.161/api/node/mo/uni/tn-TEST_TNT_TEST-01.json"%(apicIP)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	TennantList = json.loads(response2.text)
	alist = []
	for i in range(len(TennantList["imdata"])):
		alist.append(TennantList["imdata"][i]["fvTenant"]["attributes"]["name"])
	return alist
	#return TennantList
################################################################################################################################################


################################################################################################################################################
#Function fetches list of tenants available within APIC reach on the Fabric
def GetTennantList():
	url2 = "https://%s/api/class/fvTenant.json"%(apicIP)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	TennantList = json.loads(response2.text)
	alist = []
	for i in range(len(TennantList["imdata"])):
		alist.append(TennantList["imdata"][i]["fvTenant"]["attributes"]["name"])
	return alist
	#return TennantList
################################################################################################################################################
#print(GetTennantList())

################################################################################################################################################
#Function fetches list of APs for given tenant
def GetAPList(tenant_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s.json?query-target=children&target-subtree-class=fvAp" %(apicIP, tenant_name)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	APListJson = json.loads(response2.text)
	alist = []
	for i in range(len(APListJson["imdata"])):
		alist.append(APListJson["imdata"][i]["fvAp"]["attributes"]["name"])
	return alist
################################################################################################################################################


################################################################################################################################################
#Function fetches list of EPGs for given tenant and application PRofile
def GetEPGList(tenant_name, apProfile):
	url2 = "https://%s/api/node/mo/uni/tn-%s.json?query-target=subtree&target-subtree-class=fvAEPg&target-subtree-class=fvAEPg=fvBD" %(apicIP,tenant_name)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	APListJson = json.loads(response2.text)
	alist = []
	for i in range(len(APListJson["imdata"])):
		alist.append(APListJson["imdata"][i]["fvAEPg"]["attributes"]["name"])
	#return APListJson
	return alist
################################################################################################################################################




################################################################################################################################################
#Function fetches list of associated EPGs for given BD 
def GetEPG4BDList(tenant_name, apProfile, BDname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/BD-%s.json?query-target=children&target-subtree-class=relnFrom" %(apicIP,tenant_name, BDname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	EPGListJson = json.loads(response2.text)
	alist = []
	for i in range(len(EPGListJson["imdata"])):
		alist.append(re.split("-", re.split("/",EPGListJson["imdata"][i]["fvRtBd"]["attributes"]["tDn"])[-1])[-1])

	return alist
################################################################################################################################################


################################################################################################################################################
#Function fetches list of associated BD for given EPG
def GetPhy4EPG(tenant_name, apProfile, EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children&target-subtree-class=fvRsDomAtt" %(apicIP,tenant_name,apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	EPGListJson = json.loads(response2.text)
	alist = []
	for i in range(len(EPGListJson["imdata"])):
		alist.append((EPGListJson["imdata"][i]["fvRsDomAtt"]["attributes"]["tDn"]).partition("phys-")[2])

	#return EPGListJson
	return alist#, EPGListJson
################################################################################################################################################

###############################################################################################################################################
#Function fetches list of associated VMM domains for given EPG
def GetVMMDomainsinEPGs(tenant_name, apProfile,EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children&target-subtree-class=fvRsDomAtt"%(apicIP, tenant_name, apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	DomainsListJson = json.loads(response2.text)
	alist = []
	for i in range(len(DomainsListJson["imdata"])):
		try:
			alist.append(DomainsListJson["imdata"][i]["fvRsDomAtt"]["attributes"]["tDn"].partition("vmmp-")[2].partition("dom-")[2])
		except:
			pass
	#remove empty elements from list
	alist = list(filter(None, alist))
	return alist
	#return DomainsListJson
################################################################################################################################################
#print(GetVMMDomainsinEPGs("tenant01","AP1","EPG1"))


################################################################################################################################################
#Function fetches list of associated BD for given EPG
def GetEPGObject(tenant_name, apProfile, EPGname):
	#URL to GET EPG primary object
	url1 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json" %(apicIP,tenant_name,apProfile,EPGname)
	#URL to GET EPG children objects
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?&query-target=children" %(apicIP,tenant_name,apProfile,EPGname)
	#Save response from both GET requests
	response1 = requests.request("GET", url1, headers=headers, verify = False)
	EPGListJson = json.loads(response1.text)['imdata'][0]
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	EPGListJson2 = json.loads(response2.text)
	#Add children objects to primary object
	(EPGListJson)["children"] = EPGListJson2['imdata']
	
	return EPGListJson
################################################################################################################################################

#print GetEPGObject("Sman5", "apProfile", "sEPG")
#payload = "{\"fvAEPg\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s\",\"name\":\"%s\",\"rn\":\"epg-%s\",\"status\":\"created\"},\"children\":[{\"fvRsBd\":{\"attributes\":{\"tnFvBDName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}},{\"fvRsApMonPol\":{\"attributes\":{\"tnMonEPGPolName\":\"default\",\"status\":\"created,modified\"},\"children\":[]}}"%(tenant_name,apProfile,EPGname,EPGname,EPGname, BDname)




################################################################################################################################################
#Function fetches list of associated BD for given VRF
def GetBD4VRF(tenant_name, vrf):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ctx-%s.json?query-target=children&target-subtree-class=relnFrom" %(apicIP,tenant_name,vrf)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	EPGListJson = json.loads(response2.text)
	alist = []
	for i in range(len(EPGListJson["imdata"])):
		try:
			alist.append(EPGListJson["imdata"][i]["fvRtCtx"]["attributes"]["tDn"].partition("BD-")[2])
		except:
			pass
	return alist#,EPGListJson
################################################################################################################################################
#print GetBD4VRF("tenant-1","tenant1-vrf1")

###############################################################################################################################################
#Function fetches list of VRFs for given tenant
def GetvrfList(tenant_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s.json?query-target=children&target-subtree-class=fvCtx"%(apicIP,tenant_name)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	vrfListJson = json.loads(response2.text)
	alist = []
	for i in range(len(vrfListJson["imdata"])):
		alist.append(vrfListJson["imdata"][i]["fvCtx"]["attributes"]["name"])
	return alist
################################################################################################################################################

###############################################################################################################################################
#Function fetches list of VRFs for given tenant
def GetBDList(tenant_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s.json?query-target=children&target-subtree-class=fvBD"%(apicIP, tenant_name)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	BDListJson = json.loads(response2.text)
	alist = []
	for i in range(len(BDListJson["imdata"])):
		alist.append(BDListJson["imdata"][i]["fvBD"]["attributes"]["name"])
	
	return alist
################################################################################################################################################

###############################################################################################################################################
#Function fetches list of static ports for given EPGs
def GetStaticPortsonEPGs(tenant_name, apProfile,EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children&target-subtree-class=fvRsPathAtt"%(apicIP, tenant_name, apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	StaticPortsListJson = json.loads(response2.text)
	alist = []
	for i in range(len(StaticPortsListJson["imdata"])):
		path = re.split('/', re.search('\[(.*)\]',StaticPortsListJson["imdata"][i]["fvRsPathAtt"]["attributes"]["dn"]).group(1))
		vlan = StaticPortsListJson["imdata"][i]["fvRsPathAtt"]["attributes"]["encap"]
		try:
			alist.append(([path[1].partition("-")[2],path[2].partition("-")[2],re.sub("]", "", path[4]), vlan.partition("-")[2]]))
		except:
			pass
	return alist#, StaticPortsListJson4
################################################################################################################################################

###############################################################################################################################################
#Function fetches list of static ports for given EPGs
def GetBD4EPG(tenant_name, apProfile,EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children"%(apicIP, tenant_name, apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	StaticPortsListJson4 = json.loads(response2.text)['imdata'][0]['fvRsBd']['attributes']['tnFvBDName']
	return StaticPortsListJson4
################################################################################################################################################
#print(GetBD4EPG("tenant01", "AP1","EPG1"))


###############################################################################################################################################
#Function fetches list of static ports for given EPGs
def GetEPGinfo(tenant_name, apProfile,EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=children"%(apicIP, tenant_name, apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	StaticPortsListJson = json.loads(response2.text)
	return StaticPortsListJson[0]
################################################################################################################################################

###############################################################################################################################################
#Function fetches list of static ports for given EPGs
def GetVLP():
	url2 = "https://%s/api/node/mo/uni/infra.json?query-target=children&query-target=subtree&target-subtree-class=fvnsVlanInstP&query-target=children&target-subtree-class=fvnsEncapBlk"%(apicIP)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	StaticPortsListJson = json.loads(response2.text)
	return StaticPortsListJson
################################################################################################################################################
#print(GetVLP())

'''
timestamp: 10:00:43 DEBUG 
method: GET
url: https://11.11.11.161/api/node/mo/uni/infra.json?query-target=subtree&target-subtree-class=fvnsVlanInstP#&query-target-filter=not(wcard(fvnsVlanInstP.dn,%22__ui_%22))&target-subtree-class=fvnsEncapBlk&query-target=subtree&rsp-subtree=full&rsp-subtree-class=tagAliasInst&subscription=yes
'''

#print GetStaticPortsonEPGs("Sman2", "apProfile","NewEPG0")

################################################################################################################################################
#Function adds Tenant to the logical topology. The argument needs to be the name of Tenant
def AddTennant(tenant_name):
	url2 = "https://%s/api/mo/uni.json"%(apicIP)
	payload = "{\"fvTenant\" : {\"attributes\" : {\"name\" : \"%s\" }}}  " %tenant_name
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	TennantList = json.loads(response2.text)
################################################################################################################################################
#print(AddTennant("arb"))

################################################################################################################################################
#Function adds BD to the logical topology. The argument needs to be the name of BD, tenant
def AddBD(BDname, tenant_name, **kwargs): #vrf is same as Context
	'''Takes 2 compulsory arguments. 
	Optional arguments parse in 
	unicaseRoute = 'true' or 'false' as optional argument to set as L3 or L2. Same for 
	L2 unknown multicast flooding L2UnknownUnicast = 'flood' or 'proxy'
	arpFlood = yes or no
	'''
	url2 = "https://%s/api/mo/uni/tn-%s.json" %(apicIP, tenant_name)
	#if kwargs['unicastRoute']: unicastRoute = kwargs['unicastRoute'] else: unicastRoute = 'true'
	unicastRoute = kwargs['unicastRoute'] if 'unicastRoute' in kwargs else 'true'
	unkMacUcastAct = kwargs['L2UnknownUnicast'] if 'L2UnknownUnicast' in kwargs else 'proxy'
	arpFlood = kwargs['arpFlood'] if 'arpFlood' in kwargs else 'no'
	payload = "{\"fvBD\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s\",\"name\":\"%s\",\"arpFlood\":\"%s\",\"unicastRoute\":\"%s\",\"unkMacUcastAct\":\"%s\",\"rn\":\"BD-%s\",\"status\":\"created,modified\"},\"children\":[]}}"%(tenant_name, BDname, BDname, arpFlood,unicastRoute,unkMacUcastAct,BDname)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################




################################################################################################################################################
#Function associates VRF to specified BD.
def AssociateVRFToBD(tenant_name, BDname, vrf): #vrf is same as Context
	url2 = "https://%s/api/mo/uni/tn-%s/BD-%s/rsctx.json" %(apicIP, tenant_name, BDname)
	payload = "{\"fvRsCtx\":{\"attributes\":{\"tnFvCtxName\":\"%s\"},\"children\":[]}}"%vrf
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function adds subnet to BD
def AddSubnetToBD(tenant_name, BDname, subnet, scope): #vrf is same as Context
	url2 = "https://%s/api/mo/uni/tn-%s/BD-%s.json" %(apicIP,tenant_name, BDname)
	payload = "{\"fvBD\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s\",\"status\":\"modified\"},\"children\":[{\"fvSubnet\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s/subnet-[%s]\",\"status\":\"created\",\"scope\":\"%s\"},\"children\":[]}}]}}"%(tenant_name, BDname, tenant_name, BDname, subnet, scope)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function adds subnet to EPG
def AddSubnetToEPG(tenant_name, apProfile, EPGname, subnet, scope): 
	url2 = "https://%s/api/mo/uni/tn-%s/ap-%s/epg-%s/subnet-[%s].json" %(apicIP,tenant_name, apProfile, EPGname, subnet)
	payload = "{\"fvSubnet\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s/subnet-[%s]\",\"ctrl\":\"unspecified\",\"ip\":\"%s\",\"scope\":\"%s\",\"rn\":\"subnet-[%s]\",\"status\":\"created\"},\"children\":[]}}"%(tenant_name, apProfile, EPGname,subnet,subnet,scope,subnet)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

#print AddSubnetToEPG("PLATFORM_MGMT_TNT","HXReplication_AP","HXReplication_EPG20","10.201.101.65/26","shared")


'''
method: POST
url: https://7.7.7.160/api/node/mo/uni/tn-PLATFORM_MGMT_TNT/ap-HXReplication_AP/epg-HXReplication_EPG10/subnet-[10.201.101.1/26].json
payload{"fvSubnet":{"attributes":{"dn":"uni/tn-PLATFORM_MGMT_TNT/ap-HXReplication_AP/epg-HXReplication_EPG10/subnet-[10.201.101.1/26]","ctrl":"unspecified","ip":"10.201.101.1/26","scope":"shared","rn":"subnet-[10.201.101.1/26]","status":"created"},"children":[]}}
response: {"totalCount":"0","imdata":[]}
################################################################################################################################################
'''
#Function adds VRF to the logical topology under a tenant
def AddVRF2Tenant(tenant_name, vrf): #vrf is same as Context
	url2 = "https://%s/api/mo/uni/tn-%s/ctx-%s.json" %(apicIP,tenant_name,vrf)
	payload = "{\"fvCtx\":{\"attributes\":{\"dn\":\"uni/tn-%s/ctx-%s\",\"name\":\"%s\",\"rn\":\"ctx-%s\",\"status\":\"created\"},\"children\":[]}}"%(tenant_name, vrf,vrf,vrf)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################


################################################################################################################################################
#Function adds EPG to the logical topology. The argument needs name of EPG and corresponding tenant_name, apProfile, BridgeDomain
def AddEPG(tenant_name, apProfile, BDname, EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s.json"%(apicIP,tenant_name, apProfile)
	payload = "{\"fvAEPg\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s\",\"name\":\"%s\",\"rn\":\"epg-%s\",\"status\":\"created\"},\"children\":[{\"fvRsBd\":{\"attributes\":{\"tnFvBDName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}},{\"fvRsApMonPol\":{\"attributes\":{\"tnMonEPGPolName\":\"default\",\"status\":\"created,modified\"},\"children\":[]}}"%(tenant_name,apProfile,EPGname,EPGname,EPGname, BDname)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function deletes EPG to the logical topology. The argument needs name of EPG and corresponding tenant_name, apProfile, BridgeDomain
def DelEPG(tenant_name, apProfile, EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s.json"%(apicIP,tenant_name, apProfile)
	payload = "{\"fvAEPg\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s\",\"name\":\"%s\",\"rn\":\"epg-%s\",\"status\":\"deleted\"}}}"%(tenant_name,apProfile,EPGname,EPGname,EPGname)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function adds EPG to the logical topology. The argument needs name of EPG and corresponding tenant_name, apProfile, BridgeDomain
def postunderAP(tenant_name, apProfile, payload):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s.json"%(apicIP,tenant_name, apProfile)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function adds EPG to the logical topology. The argument needs name of EPG and corresponding tenant_name, apProfile, BridgeDomain
def AddAP(tenant_name, apProfile):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s.json"%(apicIP,tenant_name, apProfile)
	payload = "{\"fvAp\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s\",\"name\":\"%s\",\"rn\":\"ap-%s\",\"status\":\"created\"}}}"%(tenant_name,apProfile,apProfile,apProfile)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function associates a Physical Domain (Fabric Access Policy) to EPG
def AssociatePhyDom2EPG(tenant_name, apProfile, EPGname, PHY):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name, apProfile,EPGname)
	payload = "{\"fvRsDomAtt\":{\"attributes\":{\"resImedcy\":\"immediate\",\"tDn\":\"uni/phys-%s\",\"status\":\"created\"},\"children\":[]}}"%(PHY)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################



################################################################################################################################################
#Function associates a BridgeDomain to EPG
def AssociateBD2EPG(tenant_name, apProfile, EPGname, BDname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name, apProfile,EPGname)
	payload = "{\"fvRsBd\":{\"attributes\":{\"tnFvBDName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}"%(BDname)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function associates a Physical Domain (Fabric Access Policy) to EPG
def AssociateVMDom2EPG(tenant_name, apProfile, EPGname, VMDom):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name, apProfile,EPGname)
	payload = "{\"fvRsDomAtt\":{\"attributes\":{\"instrImedcy\":\"immediate\",\"resImedcy\":\"pre-provision\",\"tDn\":\"uni/vmmp-VMware/dom-%s\",\"status\":\"created,modified\"},\"children\":[]}}"%(VMDom)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function adds Static Port association to EPG
def AssociateStaticPort2EPG(tenant_name, apProfile, EPGname, Vlan, pod,leafpath,port):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name, apProfile,EPGname)
	payload = "{\"fvRsPathAtt\":{\"attributes\":{\"encap\":\"vlan-%s\",\"tDn\":\"topology/pod-%s/paths-%s/pathep-[eth1/%s]\",\"status\":\"created\"},\"children\":[]}}"%(Vlan, pod, leafpath, port)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################


################################################################################################################################################
#Function adds Static Port association to EPG
def AssociateVPCPort2EPG(tenant_name, apProfile, EPGname, Vlan, pod,leafpath,port):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name, apProfile,EPGname)
	payload = "{\"fvRsPathAtt\":{\"attributes\":{\"encap\":\"vlan-%s\",\"tDn\":\"topology/pod-%s/protpaths-%s/pathep-[%s]\",\"status\":\"created\"},\"children\":[]}}"%(Vlan, pod, leafpath, port)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################




################################################################################################################################################
#Function adds VLAN pool to Fabric. Arguments needed: VLP name, range from, range to, allocation mode (dynamic/static).
def addVLP(VLP_name, rangeFrom, rangeTo, allocationMode):
	url2 = "https://%s/api/node/mo/uni/infra/vlanns-[%s]-%s.json"%(apicIP,VLP_name, allocationMode)

	payload = "{\"fvnsVlanInstP\":{\"attributes\":{\"dn\":\"uni/infra/vlanns-[%s]-%s\",\"name\":\"%s\",\"rn\":\"vlanns-[%s]-%s\",\"status\":\"created\"},\"children\":[{\"fvnsEncapBlk\":{\"attributes\":{\"dn\":\"uni/infra/vlanns-[%s]-%s/from-[vlan-%s]-to-[vlan-%s]\",\"from\":\"vlan-%s\",\"to\":\"vlan-%s\",\"allocMode\":\"%s\",\"rn\":\"from-[vlan-%s]-to-[vlan-%s]\",\"status\":\"created\"}}}]}}"%(VLP_name,allocationMode,VLP_name,VLP_name,allocationMode,VLP_name,allocationMode,rangeFrom,rangeTo,rangeFrom,rangeTo,allocationMode,rangeFrom,rangeTo)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################


################################################################################################################################################
#Function creates and attaches AEP to specified PhysicalDomain. Name of AEP and Phys domain name needed for argument
def attachAEP(AEP_name, Phy_name):
	url2 = "https://%s/api/node/mo/uni/infra.json"%(apicIP)
	payload = "{\"infraInfra\":{\"attributes\":{\"dn\":\"uni/infra\",\"status\":\"modified\"},\"children\":[{\"infraAttEntityP\":{\"attributes\":{\"dn\":\"uni/infra/attentp-%s\",\"name\":\"%s\",\"rn\":\"attentp-%s\",\"status\":\"created\"},\"children\":[{\"infraRsDomP\":{\"attributes\":{\"tDn\":\"uni/phys-%s\",\"status\":\"created\"},\"children\":[]}}]}},{\"infraFuncP\":{\"attributes\":{\"dn\":\"uni/infra/funcprof\",\"status\":\"modified\"}}}]}}"%(AEP_name,AEP_name,AEP_name,Phy_name)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################

################################################################################################################################################
#Function creates PhysicalDomain and associates with VLP. Name of VLP and Phys domain name needed for argument
def createPHY(Phy_name, VLP_name):
	url2 = "https://%s/api/node/mo/uni/phys-%s.json"%(apicIP,Phy_name)#, apProfile,EPGname)

	payload = "{\"physDomP\":{\"attributes\":{\"dn\":\"uni/phys-%s\",\"name\":\"%s\",\"rn\":\"phys-%s\",\"status\":\"created\"},\"children\":[{\"infraRsVlanNs\":{\"attributes\":{\"tDn\":\"uni/infra/vlanns-[%s]-dynamic\",\"status\":\"created\"},\"children\":[]}}]}}"%(Phy_name,Phy_name,Phy_name,VLP_name)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################



def createVPCPolGrp(VPCPolGrpName, AEP, **kwargs):
	'''Creates a VPCPolGrp using defaults for CDP, LLDP, and LACP.
		2 Compulsory arguments in this order: VPC Policy Group name, AEP
		Optional keyword arguments: CDP = "", LLDP= "", LACP = ""
		If you want to change these to different policies, then please parse in
		the name of the policies as optional arguments. For e.g. 
		createVPCPolGrp("myVPCPolGrp","myAEP", CDP="CDP_enable", LLDP="LLDP_enable", LACP="LACP_active")
		
		Please note that the policies will have to be preconfigured (i.e. LLDP_enable must be a policy) for the optional
		arguments to work. 
		You don't have to use all optional arguments.'''
	
	url2 = "https://%s/api/node/mo/uni/infra/funcprof/accbundle-%s.json"%(apicIP,VPCPolGrpName)#, apProfile,EPGname)
	
	LLDP = kwargs['LLDP'] if 'LLDP' in kwargs else  "default"
	CDP = kwargs['CDP'] if 'CDP' in kwargs else 'default'
	LACP = kwargs['LACP'] if 'LACP' in kwargs else 'default'	
	
	payload = "{\"infraAccBndlGrp\":{\"attributes\":{\"dn\":\"uni/infra/funcprof/accbundle-%s\",\"lagT\":\"node\",\"name\":\"%s\",\"rn\":\"accbundle-%s\",\"status\":\"created\"},\"children\":[{\"infraRsAttEntP\":{\"attributes\":{\"tDn\":\"uni/infra/attentp-%s\",\"status\":\"created,modified\"},\"children\":[]}},{\"infraRsLacpPol\":{\"attributes\":{\"tnLacpLagPolName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}},{\"infraRsCdpIfPol\":{\"attributes\":{\"tnCdpIfPolName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}},{\"infraRsLldpIfPol\":{\"attributes\":{\"tnLldpIfPolName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}}"%(VPCPolGrpName,VPCPolGrpName,VPCPolGrpName,AEP,LACP,CDP,LLDP)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def createIntPolGrp(IntPolGrpName, AEP_name, **kwargs):
	'''Creates a interface PolGrp using defaults for CDP, LLDP
		2 Compulsory arguments in this order: VPC Policy Group name, AEP
		Optional keyword arguments: CDP = "", LLDP= ""
		If you want to change these to different policies, then please parse in
		the name of the policies as optional arguments. For e.g. 
		createVPCPolGrp("myVPCPolGrp","myAEP", CDP="CDP_enable", LLDP="LLDP_enable")
		
		Please note that the policies will have to be preconfigured (i.e. LLDP_enable must be a policy) for the optional
		arguments to work. 
		You don't have to use all optional arguments.'''
	
	url2 = "https://%s/api/node/mo/uni/infra/funcprof/accportgrp-%s.json"%(apicIP,IntPolGrpName)#, apProfile,EPGname)
	
	LLDP = kwargs['LLDP'] if 'LLDP' in kwargs else  "default"
	CDP = kwargs['CDP'] if 'CDP' in kwargs else 'default'

	
	payload = "{\"infraAccPortGrp\":{\"attributes\":{\"dn\":\"uni/infra/funcprof/accportgrp-%s\",\"name\":\"%s\",\"rn\":\"accportgrp-%s\",\"status\":\"created\"},\"children\":[{\"infraRsAttEntP\":{\"attributes\":{\"tDn\":\"uni/infra/attentp-%s\",\"status\":\"created,modified\"},\"children\":[]}},{\"infraRsCdpIfPol\":{\"attributes\":{\"tnCdpIfPolName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}},{\"infraRsLldpIfPol\":{\"attributes\":{\"tnLldpIfPolName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}}"%(IntPolGrpName,IntPolGrpName,IntPolGrpName,AEP_name,CDP,LLDP)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)


def createIntProf(IntProfName):
	'''Creates a IntProfName. Only argument taken in is the name of the interface Profile.
	'''
	
	url2 = "https://%s/api/node/mo/uni/infra/accportprof-%s.json"%(apicIP,IntProfName)#, apProfile,EPGname)	
	payload = '{"infraAccPortP":{"attributes":{"dn":"uni/infra/accportprof-%s","name":"%s","rn":"accportprof-%s","status":"created,modified"},"children":[]}}'%(IntProfName,IntProfName,IntProfName)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def AddPortSeltoIntProf(IntProfName,PortSelectorName,Port,PolGrp):
	'''Adds Ports to InterfaceProfile. Compulsory arguments in following order:
	IntProfName: This profile must exist already
	PortSelectorName: Choose a name for the new port selector you want to create
	Port: Which port do you want to associate? Just the number. Do not use 1/27, use 27.
	AEP: Which AEP to be assocaited to
	'''
	
	url2 = "https://%s/api/node/mo/uni/infra/accportprof-%s/hports-%s-typ-range.json"%(apicIP,IntProfName, PortSelectorName)#, apProfile,EPGname)
	
	payload = '{"infraHPortS":{"attributes":{"dn":"uni/infra/accportprof-%s/hports-%s-typ-range","name":"%s","rn":"hports-%s-typ-range","status":"created,modified"},"children":[{"infraPortBlk":{"attributes":{"dn":"uni/infra/accportprof-%s/hports-%s-typ-range/portblk-block2","fromPort":"%s","toPort":"%s","name":"block2","rn":"portblk-block2","status":"created,modified"},"children":[]}},{"infraRsAccBaseGrp":{"attributes":{"tDn":"uni/infra/funcprof/accportgrp-%s","status":"created,modified"},"children":[]}}]}}'%(IntProfName,PortSelectorName,PortSelectorName,PortSelectorName,IntProfName,PortSelectorName,Port,Port,PolGrp)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def DeletePortSeltoInt(IntProfName,PortSelectorName):
	'''Deletes portselectors to a given Interface profile
	'''
	url2 = "https://%s/api/node/mo/uni/infra/accportprof-%s/hports-%s-typ-range.json"%(apicIP,IntProfName, PortSelectorName)
	payload = '{\"infraHPortS\":{\"attributes\":{\"dn\":\"uni/infra/accportprof-%s/hports-%s-typ-range\",\"status\":\"deleted\"},\"children\":[]}}'%(IntProfName,PortSelectorName)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)


def createSwitchProf(SwitchProfName):
	'''Creates a Switch Profile. Only argument taken in is the name of the Switch Profile.
	'''
	
	url2 = "https://%s/api/node/mo/uni/infra//nprof-%s.json"%(apicIP,SwitchProfName)#, apProfile,EPGname)	
	payload = '{"infraNodeP":{"attributes":{"dn":"uni/infra/nprof-%s","name":"%s","rn":"nprof-%s","status":"created,modified"},"children":[]}}'%(SwitchProfName,SwitchProfName,SwitchProfName)	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)



def AddLeafSeltoSwitchProf(SwitchProfName,SwitchSelectorName,Switch, **kwargs):
	'''Adds switches to Switch Profile. Compulsory arguments in following order:
	SwitchProfName: This profile must exist already
	SwitchSelectorName: Choose a name for the new Switch selector you want to create
	Switch: Which port do you want to associate? Just the number. For e.g. 101
	Kwargs: if you want a switch based AEP. Functionality to be added later
	'''
	
	url2 = "https://%s/api/node/mo/uni/infra/nprof-%s/leaves-%s-typ-range.json"%(apicIP,SwitchProfName, SwitchSelectorName)#, apProfile,EPGname)
	
	payload = '{"infraLeafS":{"attributes":{"dn":"uni/infra/nprof-%s/leaves-%s-typ-range","type":"range","name":"%s","status":"created","rn":"leaves-%s-typ-range"},"children":[{"infraNodeBlk":{"attributes":{"dn":"uni/infra/nprof-%s/leaves-%s-typ-range/nodeblk-7bd8170e51d90b40","from_":"%s","to_":"%s","status":"created"},"children":[]}}]}}'%(SwitchProfName,SwitchSelectorName,SwitchSelectorName,SwitchSelectorName,SwitchProfName,SwitchSelectorName,Switch,Switch)
	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)


def addIntProfToSwitchProf(SwitchProfName, IntProfName):
	'''Adds an existing InterfaceProfile to a Switch Profile. Compulsory arguments in this order -> switch profile name, interface profile name
	'''
	
	url2 = "https://%s/api/node/mo/uni/infra//nprof-%s.json"%(apicIP,SwitchProfName)#, apProfile,EPGname)	
	payload = '{"infraRsAccPortP":{"attributes":{"tDn":"uni/infra/accportprof-%s","status":"created,modified"},"children":[]}}'%(IntProfName)	
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def createContractandAssociate(tenant_name,apProfile,provEPG,conEPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s.json"%(apicIP,tenant_name)#, apProfile,EPGname)
	payload = "{\"fvTenant\":{\"attributes\":{\"dn\":\"uni/tn-%s\",\"status\":\"modified\"},\"children\":[{\"fvAp\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s\",\"status\":\"modified\"},\"children\":[{\"fvAEPg\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s\",\"status\":\"modified\"},\"children\":[{\"fvRsProv\":{\"attributes\":{\"tnVzBrCPName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}},{\"fvAEPg\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s\",\"status\":\"modified\"},\"children\":[{\"fvRsCons\":{\"attributes\":{\"tnVzBrCPName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}}]}},{\"vzBrCP\":{\"attributes\":{\"dn\":\"uni/tn-%s/brc-%s\",\"name\":\"%s\",\"scope\":\"tenant\",\"status\":\"created\"},\"children\":[{\"vzSubj\":{\"attributes\":{\"dn\":\"uni/tn-%s/brc-%s/subj-Subject\",\"name\":\"Subject\",\"status\":\"created\"},\"children\":[{\"vzRsSubjFiltAtt\":{\"attributes\":{\"tnVzFilterName\":\"default\",\"status\":\"created,modified\"},\"children\":[]}}]}}]}}]}}"%(tenant_name,tenant_name,apProfile,tenant_name,apProfile,provEPG,contract_name,tenant_name,apProfile,conEPG,contract_name,tenant_name,contract_name,contract_name,tenant_name,contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)


def GetContractList(tenant_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s.json?query-target=children&target-subtree-class=vzBrCP"%(apicIP,tenant_name)#, apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	listOfContracts = [v['vzBrCP']['attributes']['name'] for v in json.loads(response2.text)['imdata']]
	return listOfContracts


def GetContractList4EPGs(tenant_name,apProfile,EPGname):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json?query-target=subtree&target-subtree-class=fvRsCons&target-subtree-class=fvRsProv"%(apicIP,tenant_name,apProfile,EPGname)#, apProfile,EPGname)
	response2 = requests.request("GET", url2, headers=headers, verify = False)
	listOfProvidedContracts = [v['fvRsProv']['attributes']['tnVzBrCPName'] for v in json.loads(response2.text)['imdata'] if 'fvRsProv' in v]
	listOfConsumedContracts = [v['fvRsCons']['attributes']['tnVzBrCPName'] for v in json.loads(response2.text)['imdata'] if 'fvRsCons' in v]
	return listOfConsumedContracts,listOfProvidedContracts
	#return json.loads(response2.text)
#print(GetContractList4EPGs("CUST_IAG_TNT_Prod-01","CUST_AP","EPG_TruApp2"))
# https://11.11.11.161/api/node/mo/uni/tn-CUST_IAG_TNT_Prod-01/ap-CUST_AP/epg-EPG_TrVOIP2.json?query-target=subtree&target-subtree-class=fvRsCons&query-target-filter=not(wcard(fvRsCons.dn,%22__ui_%22))&target-subtree-class=fvRsConsIf,fvRsProtBy,fvRsProv,vzConsSubjLbl,vzProvSubjLbl,vzConsLbl,vzProvLbl,fvRsIntraEpg&query-target=subtree&subscription=yes

def AssociateEPGasProvider(tenant_name,apProfile,EPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name,apProfile,EPG)#, apProfile,EPGname)
	payload = "{\"fvRsProv\":{\"attributes\":{\"tnVzBrCPName\":\"%s\",\"status\":\"created\"},\"children\":[]}}"%(contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def AssociateEPGasConsumer(tenant_name,apProfile,EPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name,apProfile,EPG)#, apProfile,EPGname)
	payload = "{\"fvRsCons\":{\"attributes\":{\"tnVzBrCPName\":\"%s\",\"status\":\"created\"},\"children\":[]}}"%(contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def DeleteEPGasProvider(tenant_name,apProfile,EPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name,apProfile,EPG)#, apProfile,EPGname)
	payload = "{\"fvRsProv\":{\"attributes\":{\"tnVzBrCPName\":\"%s\",\"status\":\"deleted\"},\"children\":[]}}"%(contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def DeleteEPGasConsumer(tenant_name,apProfile,EPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name,apProfile,EPG)#, apProfile,EPGname)
	payload = "{\"fvRsCons\":{\"attributes\":{\"tnVzBrCPName\":\"%s\",\"status\":\"deleted\"},\"children\":[]}}"%(contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)


'''
method: POST
url: https://11.11.11.161/api/node/mo/uni/tn-tenant01/ap-AP1/epg-EPG1/rsprov-fs.json
payload{"fvRsProv":{"attributes":{"dn":"uni/tn-tenant01/ap-AP1/epg-EPG1/rsprov-fs","status":"deleted"},"children":[]}}
response: {"totalCount":"0","imdata":[]}
timestamp: 15:22:47 DEBUG 
'''
def AssociateEPGasConsumertoExternal(tenant_name,apProfile,EPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json"%(apicIP,tenant_name,apProfile,EPG)#, apProfile,EPGname)
	payload = "{\"fvRsConsIf\":{\"attributes\":{\"tnVzCPIfName\":\"%s\",\"status\":\"created\"},\"children\":[]}}"%(contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)

def SetL3OutasProviderContract(tenant_name,apProfile,EPG,contract_name):
	url2 = "https://%s/api/node/mo/uni/tn-%s/out-%s/instP-%s.json"%(apicIP,tenant_name,L3outname,networkname)#, apProfile,EPGname)
	payload = "{\"fvRsProv\":{\"attributes\":{\"tnVzBrCPName\":%s,\"status\":\"created,modified\"},\"children\":[]}}"%(contract_name)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)


def addAdminUser(username,firstname,lastname,password):
	'''
	This function creates a new admin user with all priveleges. Please pass in the arguments in the following order:
	username,	firstname,	lastname,	password)
	They are all compusory.
	'''
	url2 = "https://%s/api/node/mo/uni/userext/user-%s.json"%(apicIP,username)#, apProfile,EPGname)
	payload = "{\"aaaUser\":{\"attributes\":{\"dn\":\"uni/userext/user-%s\",\"name\":\"%s\",\"pwd\":\"%s\",\"firstName\":\"%s\",\"lastName\":\"%s\",\"accountStatus\":\"active\",\"rn\":\"user-%s\",\"status\":\"created\"},\"children\":[{\"aaaUserDomain\":{\"attributes\":{\"dn\":\"uni/userext/user-%s/userdomain-all\",\"name\":\"all\",\"status\":\"created,modified\"},\"children\":[{\"aaaUserRole\":{\"attributes\":{\"dn\":\"uni/userext/user-%s/userdomain-all/role-admin\",\"name\":\"admin\",\"privType\":\"writePriv\",\"status\":\"created,modified\"},\"children\":[]}}]}}]}}"%(username,username,password,firstname,lastname,username,username,username)
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)



################################################################################################################################################
#Function creates Interface Policy group and associates with AEP.
def createInterfacePolGrp(PolGrp_name, AEP_name):
	ApicCooky = getCookie(url,username,password)
	url2 = "https://7.7.7.160/api/node/mo/uni/infra/funcprof/accportgrp-%s.json"%(PolGrp_name)
	headers = {
	    'Content-Type': "application/json",
	    'Accept': "application/json",
	    'cookie': "APIC-cookie=%s" %ApicCooky,
	    'Cache-Control': "no-cache",
	        }


#	payload{"infraAccPortGrp":{"attributes":{"dn":"uni/infra/funcprof/accportgrp-SManLEAFPolGrp","name":"SManLEAFPolGrp","rn":"accportgrp-SManLEAFPolGrp","status":"created"},"children":[{"infraRsAttEntP":{"attributes":{"tDn":"uni/infra/attentp-smanAEP","status":"created,modified"},"children":[]}},{"infraRsHIfPol":{"attributes":{"tnFabricHIfPolName":"default","status":"created,modified"},"children":[]}},{"infraRsCdpIfPol":{"attributes":{"tnCdpIfPolName":"cdp-dis","status":"created,modified"},"children":[]}},{"infraRsLldpIfPol":{"attributes":{"tnLldpIfPolName":"lldp-ena","status":"created,modified"},"children":[]}}]}}

	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	return json.loads(response2.text)
################################################################################################################################################


################################################################################################################################################
#Function adds Tenant to the logical topology. The argument needs to be the name of Tenant
def DeleteTennant(tenant_name):
	url2 = "https://%s/api/mo/uni.json"%(apicIP)
	payload = "{\"fvTenant\" : {\"attributes\" : {\"name\" : \"%s\",\"status\" : \"deleted\" }}}  " %tenant_name
	response2 = requests.request("POST", url2, data=payload, headers=headers, verify = False)
	TennantList = json.loads(response2.text)
################################################################################################################################################
#print(DeleteTennant(PLATFORM_MGMT_TNT))



'''
#Create Interface Profile (selected ports)
method: POST
url: https://X.X.X.X/api/node/mo/uni/infra/accportprof-int-prof-1_39_40_SMan.json
payload{"infraAccPortP":{"attributes":{"dn":"uni/infra/accportprof-int-prof-1_39_40_SManad","name":"int-prof-1_39_40_SMan","rn":"accportprof-int-prof-1_39_40_SMan","status":"created,modified"},"children":[{"infraHPortS":{"attributes":{"dn":"uni/infra/accportprof-int-prof-1_39_40_SMan/hports-2host3172-typ-range","name":"2host3172","rn":"hports-2host3172-typ-range","status":"created,modified"},"children":[{"infraPortBlk":{"attributes":{"dn":"uni/infra/accportprof-int-prof-1_39_40_SMan/hports-2host3172-typ-range/portblk-block2","fromPort":"39","toPort":"40","name":"block2","rn":"portblk-block2","status":"created,modified"},"children":[]}},{"infraRsAccBaseGrp":{"attributes":{"tDn":"uni/infra/funcprof/accportgrp-SManLEAFPolGrp","status":"created,modified"},"children":[]}}]}}]}}
#Create Switch Profile and associate with Interface Profile
method: POST
url: https://X.X.X.X/api/node/mo/uni/infra/nprof-101_SMan.json
payload{"infraNodeP":{"attributes":{"dn":"uni/infra/nprof-101_SMan","name":"101_SMan","rn":"nprof-101_SMan","status":"created,modified"},"children":[{"infraRsAccPortP":{"attributes":{"tDn":"uni/infra/accportprof-int-prof-1_39_40_SMan","status":"created,modified"},"children":[]}}]}}
#print createPHY("TestS","SManVLP")
#print attachAEP("smanAEP", "SMan")
#print addVLP("s", "1010","1010","dynamic")
#print GetTennantList()
x = GetTennantList()
f = open("demofile.txt", "w")
f.write(str(x))
'''
