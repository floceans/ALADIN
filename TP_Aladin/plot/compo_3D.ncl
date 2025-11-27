; Loading common environment features
load "$NCLDIR/functions/load_env.ncl"


; Partie a modifier
YEAR=2008
path_track = "../tracks/ATL/"
path_data="/scratch/work/becks/ALADIN/ANTILLES-12-BS-10ans/outputs/assembled/"
path_dsn="/scratch/work/chauvin/UEclimat_2024/TP-ATL/COMPO/"
;********************************
; select sub-regions
;********************************
  minlat =    7.0	; deg N
  maxlat =    30.0	; deg N
  minlon =  280.0	; - deg E = deg W
  maxlon =  330.0	; - deg E = deg W
; Fin de partie a modifier

YP1=YEAR+1  

VAR="ta"
data_name=VAR


;**********************************
; Definition of tracking conditions
;**********************************
VOR	=	5
RES	=	17
T	=	1
PT	=	-2
PW	=	5
REL=200

LARG  =      20
vtrsh=0.

file_ref=path_data+data_name+"_DOM12_CNRM-CM6-1-HR_amip_r1i1p1f2_CNRM-ALADIN63_v1_6hrPt_"+YEAR+"01010600-"+YP1+"01010000.nc"
print("file_ref="+file_ref)
fref = addfile(file_ref,"r")
latitude = fref->lat(:,150)
longitude = fref->lon(100,:)
level = fref->plev
;longitude=longitude+360.
nlat=dimsizes(latitude)
nlon=dimsizes(longitude)
nlev=dimsizes(level)


  nstot=0
  file_dsn="compo_"+data_name+"."+vtrsh+"."+YEAR+".vor"+VOR+"_v"+RES+"_t"+T+"_pt"+PT+"_pw"+PW+".rel"+REL+".nc"

  tccomp=new((/200,nlev,2*LARG+1,2*LARG+1/),"float")
  tcnum=new((/200/),"float")
  tciech=new((/200/),"float")
  latcomp=new((/200/),"float")
  loncomp=new((/200/),"float")
  datcomp=new((/200/),"float")
  iech=0
    ftck=path_track+"track_TP_"+YEAR+"-"+YP1+".vor"+VOR+"_res"+RES+"_"+T+"_"+PT+"_"+PW+".rel"+REL+".nc"
    print(ftck)
    trck = addfile(ftck,"r")
    latf=trck->latitude
    lonf=trck->longitude
    timf=trck->time
    nech=trck->nech
    vmax=trck->vmax
    pmin=trck->pmin
; On recupere l'annee de chaque trajectoire
    ftim=ut_calendar(timf,0)
    nstorm=dimsizes(nech)

;===============================================================================

    file_data=path_data+data_name+"_DOM12_CNRM-CM6-1-HR_amip_r1i1p1f2_CNRM-ALADIN63_v1_6hrPt_"+YEAR+"01010600-"+YP1+"01010000.nc"
    g=addfile(file_data,"r")
    level = g->plev
    nlev=dimsizes(level)

;==================================================================
;Construction du champs de sortie a partir des donnees de BestTrack
;==================================================================
    year=floattoint(ftim(:,:,0))
    month=floattoint(ftim(:,:,1))
    day=floattoint(ftim(:,:,2))
    hour=floattoint(ftim(:,:,3))
    minute=floattoint(ftim(:,:,4))
    second=floattoint(ftim(:,:,5))


  timeunit="days since 1850-01-01 00:00:00"
	
; On transpose la date TC a l'annee courante
    date = ut_inv_calendar(year,month,day,hour,minute,second,timeunit, 0)
    iftim=doubletointeger(date)

  print(nech)
  do id=0,nstorm-1
    numech=nech(id)
    do ie=0,nech(id)-1
      loncyc=lonf(id,ie)
      latcyc=latf(id,ie)
      if (((loncyc-4).gt.minlon).and.((loncyc+4).lt.maxlon)) then
      if (((latcyc-4).gt.minlat).and.((latcyc+4).lt.maxlat)) then
;      if (vmax(id,ie).gt.vtrsh) then
      jlat = ind_nearest_coord (latcyc,latitude,0)
      jlon = ind_nearest_coord (loncyc,longitude,0)
print(loncyc+"    "+latcyc+"    "+jlon+"    "+jlat)
      lon = longitude(jlon-LARG:jlon+LARG)
      lat = latitude(jlat-LARG:jlat+LARG)

      print(id+" "+ie+" "+date(id,ie))
      vou = g->$data_name$({date(id,ie)},:,jlat-LARG:jlat+LARG,jlon-LARG:jlon+LARG)

      rr0=vou

      rr0!0="lev"
      rr0!1="lat"
      rr0!2="lon"
        
      rr0&lat=latitude(jlat-LARG:jlat+LARG)
      rr0&lon=longitude(jlon-LARG:jlon+LARG)


;      if (latcyc.lt.30.) then
	 tccomp(iech,:,:,:) = rr0
	 tcnum(iech) = id
	 tciech(iech) = ie
	 latcomp(iech)= latcyc
	 loncomp(iech)= loncyc
	 datcomp(iech)=doubletofloat(date(id,ie))
	 iech=iech+1
;      end if
         delete(rr0)
;      end if
      end if
      end if
    end do
;    delete([/latf,lonf,timf,nech,vmax,pmin/])
;    delete([/ftim,year,month,day,hour,minute,second,date,iftim/])

  end do
delete(nech)


nech=iech-1
delete(nstorm)
;=======================================================================================
; On redefinit la dimension des champs en fonction du nombre de situations selectionnées
;=======================================================================================

tccomp!0="nech"
tccomp!1="level"
tccomp!2="latitude"
tccomp!3="longitude"
;=======================
; Ecriture des resultats
;=======================
iter = fspan(0,iech-1,iech)
latbox = tccomp&latitude
lonbox = tccomp&longitude
latbox = fspan(-LARG/2,LARG/2,2*LARG+1)
lonbox = fspan(-LARG/2,LARG/2,2*LARG+1)
levbox = tccomp&level
tccomp&latitude=latbox
tccomp&longitude=lonbox
tccomp&level=levbox

out=systemfunc("/bin/rm -f "+path_dsn+file_dsn)
gout = createCOMPO3D(path_dsn+file_dsn,iter,levbox,latbox,lonbox)
printVarSummary(tccomp)

dimNames = (/ "nech",  "level", "latitude", "longitude"/)  
dimSizes = (/ -1   ,  nlev, nlat,  nlon /) 
dimUnlim = (/ True , False, False, False /)   
filedimdef(gout,dimNames,dimSizes,dimUnlim)
filevardef(gout, "tccomp"    ,typeof(tccomp)  ,(/ "nech","level","latitude","longitude"/))
filevardef(gout, "tcnum"    ,typeof(tcnum)  ,(/ "nech"/))
filevardef(gout, "tciech"    ,typeof(tciech)  ,(/ "nech"/))
filevardef(gout, "latcomp"    ,typeof(latcomp)  ,(/ "nech"/))
filevardef(gout, "loncomp"    ,typeof(loncomp)  ,(/ "nech"/))
filevardef(gout, "datcomp"    ,typeof(datcomp)  ,(/ "nech"/))

gout->tccomp = (/tccomp(:nech,:,:,:)/)
gout->tcnum = (/tcnum(:nech)/)
gout->tciech = (/tciech(:nech)/)
gout->latcomp = (/latcomp(:nech)/)
gout->loncomp = (/loncomp(:nech)/)
gout->datcomp = (/datcomp(:nech)/)


