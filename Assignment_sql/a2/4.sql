.print Question4 - zijun4
SELECT rid, email, pickup, dropoff,rno
FROM requests rq, rides rd
WHERE date(rq.rdate) = date(rd.rdate) and rd.price <= rq.amount
INTERSECT
SELECT rid, email, pickup, dropoff,rno
from requests rq, rides rd, locations lo1, locations lo2
WHERE rq.pickup = lo1.lcode and rd.src = lo2.lcode and lo1.city = lo2.city
INTERSECT 
SELECT rid, email, pickup, dropoff,rno
from requests rq, rides rd, locations lo1, locations lo2
WHERE rq.dropoff = lo1.lcode and rd.dst = lo2.lcode and lo1.city = lo2.city;
