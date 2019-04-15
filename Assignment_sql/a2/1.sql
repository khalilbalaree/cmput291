.print Question1 - zijun4
SELECT m.name, m.email
FROM cars c1, cars c2, members m
WHERE c1.owner = c2.owner and c1.cno <> c2.cno and c1.owner = m.email
INTERSECT
SELECT m.name, m.email
FROM members m, rides rd, cars c
WHERE m.email = c.owner and c.cno = rd.cno;
