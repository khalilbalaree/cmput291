.print Question9 - zijun4
CREATE VIEW ride_info(rno, booked, available, rdate, price, src, dst)
AS SELECT rno, ifnull(booked, 0), seats - ifnull(booked, 0), rdate, price, lo1.city, lo2.city
FROM rides rd, locations lo1, locations lo2
LEFT OUTER JOIN 
(SELECT rno, count(*) as booked
FROM bookings
GROUP BY rno) USING (rno)
WHERE lo1.lcode = rd.src and lo2.lcode = rd.dst and date(rdate) >= date('now');