.print Question8 - zijun4
SELECT driver
FROM rides rd, locations lo
WHERE rd.dst = lo.lcode and lo.prov = 'Alberta' and date(rdate) >= '2016-01-01'
GROUP BY driver
HAVING 2 * count(*) > (SELECT count(*)
                        FROM locations
                        WHERE prov = 'Alberta');