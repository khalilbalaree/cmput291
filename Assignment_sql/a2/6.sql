.print Question6 - zijun4
SELECT DISTINCT(city), prov, ifnull(fromcity, 0), ifnull(tocity, 0), ifnull(enroutecity, 0)
FROM locations
LEFT OUTER JOIN 
(SELECT city, count(*) as fromcity
FROM locations lo, rides rd
WHERE rd.src = lo.lcode
GROUP BY city)
USING (city)
LEFT OUTER JOIN 
(SELECT city, count(*) as tocity
FROM locations lo, rides rd
WHERE rd.dst = lo.lcode
GROUP BY city) USING (city) 
LEFT OUTER JOIN 
(SELECT city, count(*) as enroutecity
FROM enroute en, locations lo
WHERE en.lcode = lo.lcode
GROUP BY city) USING (city)
WHERE fromcity is not null or tocity is not null or enroutecity is not null;