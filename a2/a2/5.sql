.print Question5 - zijun4
SELECT city, prov
FROM rides rd, locations lo
WHERE rd.dst = lo.lcode
GROUP BY prov, city
ORDER BY count(*) DESC
LIMIT 3;