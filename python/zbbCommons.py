 
class zbblabel:
  """labels used in the PAT configuration"""
  allmuonslabel="allMuons"
  muonlabel="matchedMuons"
  allelectronslabel="allElectrons"
  electronlabel="matchedElectrons"
  jetlabel="cleanPatJets"
  zmumulabel="zmuMatchedmuMatched"
  #zmumulabel="zmuAllmuAll"
  zelelabel="zelMatchedelMatched"
  #zelelabel="zelAllelAll"
  vertexlabel="goodPV"
  pulabel="addPileupInfo"
  triggerlabel="patTriggerEvent"
  metlabel="patType01SCorrectedPFMet"
  zmmbblabel="Zmmbb"
  zeebblabel="Zeebb"
  bblabel ="bbbar"
  genlabel="genParticles"

class zbbsystematics:
  SF_uncert="mean" ## choose among min/max/mean
  #SF_running_mode= "hardcoded" ## choose between hardcoded/database
  SF_running_mode= "database" ## choose between hardcoded/database
  JERfactor = 1. # 1 = recommended smearing
  JESfactor = 0. # 1 = +1sigma

class zbbfile:
  """files containing calibrations and other data"""
  ssvperfData="../data/performance_ssv_witheff_062012.root"
  pileupData="../data/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON_v2_pileupTruth.root"
  pileupMC="../data/Fall11_PU_MC.root"
  jecUncertainty="../data/JEC11_V12_AK5PF_UncertaintySources.txt"

  controlPlots="controlPlots.root"
  rooDataset="File_rds_zbb.root"


class zbbnorm:
  """information to be used for the MC sample normalization"""
  lumi_tot2011=5.21 #in fb-1
  
  #x_section 7 TeV in pb
  #https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
  xsec_DYjets_7TeV= 3048.     #Ml+l->50, NNLO for Z->ll
  xsec_TTjets_7TeV=  157.5    #NLO inclusive
  xsec_TTlept_7TeV=   16.7    #ttbar->llvvbb_
  xsec_ZZ_7TeV    =    6.206  #cms measurement EWK-11-010 (2011)
  xsec_ZH115_7TeV =    0.0300 #ZHxsec"0.4107", BR(H->bb)"0.703"
  xsec_ZH120_7TeV =    0.0242 #ZHxsec"0.3598", BR(H->bb)"0.648" 
  xsec_ZH125_7TeV =    0.0189 #ZHxsec"0.3158"*BR(H->bb)"0.577"*BR(Z->ll)"0.10399" , here l=e, mu or tau : https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CrossSections#Higgs_cross_sections_at_7_8_and
  xsec_ZH130_7TeV =    0.0143 #ZHxsec"0.2778", BR(H->bb)"0.494" 
  xsec_ZH135_7TeV =    0.0103 #ZHxsec"0.2453", BR(H->bb)"0.404" 
  xsec_tW_7TeV    =    5.3    #NLO inclusive
  xsec_tbarW_7TeV =    5.3    #NLO inclusive
  
  #x_section 8 TeV in pb, yet under construction, to be checked later
  #https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV
  xsec_DYjets_8TeV=3503.71  #Ml+l->50, NNLO for Z->ll
  xsec_TTjets_8TeV=225.197  #NLO inclusive
  xsec_ZZ_8TeV= 8.25561     #NLO inclusive Ml+l->12
  xsec_ZH125_8TeV=0.0237    #ZHxsec"0.3943 "*BR(H->bb)"0.577"*BR(Z->ll)"0.10399" , here l=e, mu or tau
  xsec_tW_8TeV=11.1         #approx. NNLO inclusive
  xsec_tbarW_8TeV=11.1      #approx. NNLO inclusive

  #number of events processed for the PATtuple production
  nev_DYjets_fall11       = 36264432 # updated
  nev_TTjets_fall11       = 59244088 # updated
  nev_ZZ_fall11       =  4191045 # updated
  nev_ZH115_fall11    =  1090000 # updated
  nev_ZH120_fall11    =  1090000 # updated
  nev_ZH125_fall11    =  1100000 # updated
  nev_ZH130_fall11    =  1100000 # updated
  nev_ZH135_fall11    =  1096956 # updated
  nev_TTpowheg_fall11 = 16352171 # if needed to be updated with matching
  nev_tW_fall11       =   814390 # updated
  nev_tbarW_fall11    =   809984 # updated
  
