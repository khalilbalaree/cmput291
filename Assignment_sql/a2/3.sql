.print Question3 - zijun4
SELECT distinct(b.email)
FROM rides rd, bookings b, locations lo1, locations lo2
where b.rno = rd.rno and lo1.lcode = rd.src and lo2.lcode = rd.dst
    and date(rd.rdate) >= "2018-11-01" 
    and date(rd.rdate) < "2018-12-01"
    and lo1.city = 'Edmonton'
    and lo2.city = 'Calgary';