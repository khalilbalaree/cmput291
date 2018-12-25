.print Question7 - zijun4
SELECT rno
FROM rides 
WHERE src in (SELECT lcode
                FROM locations
                WHERE city = 'Edmonton')
    and dst in (SELECT lcode
                FROM locations
                WHERE city = 'Calgary')
    and date(rdate) >= "2018-10-01" 
    and date(rdate) < "2018-11-01"
    and rno in (SELECT rno
                    FROM rides
                    EXCEPT
                    SELECT b.rno
                    FROM bookings b, rides rd
                    WHERE b.rno = rd.rno and b.seats = rd.seats)
    and price = (SELECT min(price)
                FROM rides 
                WHERE src in (SELECT lcode
                            FROM locations
                            WHERE city = 'Edmonton')
                and dst in (SELECT lcode
                            FROM locations
                            WHERE city = 'Calgary')
                and date(rdate) >= "2018-10-01" 
                and date(rdate) < "2018-11-01"
                and rno in (SELECT rno
                                FROM rides
                                EXCEPT
                                SELECT b.rno
                                FROM bookings b, rides rd
                                WHERE b.rno = rd.rno and b.seats = rd.seats));
