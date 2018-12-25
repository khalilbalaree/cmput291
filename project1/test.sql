select rides.rno 
from rides,enroute 
where enroute.rno=rides.rno and (src = ? or dst = ? or enroute.lcode=? )
union 
select rides.rno 
from locations, rides 
where (src=lcode or dst=lcode) and (city like ? or prov like ? or address like ?);