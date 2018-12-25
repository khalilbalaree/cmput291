.print Question10 - zijun4
SELECT ride_info.rno, booked, available, ride_info.rdate, ride_info.price, ride_info.src, ride_info.dst, rd.driver, julianday('2019-01-01') - julianday(ride_info.rdate)
FROM ride_info, rides rd
WHERE ride_info.src = 'Edmonton' and ride_info.dst = 'Calgary'
    and ride_info.rno = rd.rno
    and date(ride_info.rdate) >= '2018-12-01' and date(ride_info.rdate) < '2019-01-01'
    and ride_info.available > 0
ORDER BY ride_info.price;