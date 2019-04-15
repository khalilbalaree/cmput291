.print Question 1 - drafiei
.echo ON
select distinct email, name
from members m, cars c1, cars c2, rides r
where m.email=c1.owner and c1.owner=c2.owner and c1.cno <> c2.cno and 
      c1.cno=r.cno;

.print Question 2 - drafiei
select name, email
from cars c, members m where c.owner=m.email
intersect
select name, m.email
from bookings b, members m where b.email=m.email
except
select name, email
from rides r, members m where r.driver=m.email;

.print Question 3 - drafiei
select distinct b.email
from bookings b, rides r, locations s, locations d
where b.rno=r.rno and r.src=s.lcode and r.dst=d.lcode and
      s.city='Edmonton' and d.city='Calgary' and strftime('%Y',r.rdate)='2018' 
      and strftime('%m',r.rdate)='11';

.print Question 4 - drafiei
select rq.rid, rq.email, pickup, dropoff, r.rno
from requests rq, rides r, locations l1, locations l2, locations l3,locations l4
where r.rdate=rq.rdate and r.price <= rq.amount and src=l1.lcode and 
      dst=l2.lcode and pickup=l3.lcode and dropoff=l4.lcode and l1.city=l3.city
      and l1.prov=l3.prov and l2.city=l4.city and l2.prov=l4.prov;

.print Question 5 - drafiei
select l.prov, l.city
from rides r, locations l
where r.dst=l.lcode
group by l.prov, l.city
order by count(*) desc
limit 3;

.print Question 6 - drafiei
select l.prov, l.city, count(distinct r1.rno), count(distinct r2.rno), 
       count(distinct e.rno)
from locations l left outer join rides r1 on l.lcode=r1.src
     left outer join rides r2 on l.lcode=r2.dst left outer join enroute e 
     on l.lcode=e.lcode
group by l.prov, l.city
having count(distinct r1.rno)>0 or count(distinct r2.rno)>0 or 
       count(distinct e.rno)>0;

.print Question 7 - drafiei
select rno
from rides r, locations l1, locations l2
where r.src=l1.lcode and r.dst=l2.lcode and l1.city='Edmonton' and
      l2.city='Calgary' and
      strftime('%Y', rdate)='2018' and strftime('%m', rdate)='10' and
      seats > (select ifnull(sum(b.seats),0) from bookings b where b.rno=r.rno)
      and price <= ( select min(price)
        from rides r2, locations l3, locations l4
        where r2.src=l3.lcode and r2.dst=l4.lcode and l3.city='Edmonton' and
        l4.city='Calgary' and
        strftime('%Y', r2.rdate)='2018' and strftime('%m', r2.rdate)='10' and
        r2.seats > (select ifnull(sum(b2.seats),0) 
                    from bookings b2 where b2.rno=r2.rno));

.print Question 8 - drafiei
select driver
from rides r, locations l
where r.dst=l.lcode and l.prov='Alberta'
group by driver
having count(distinct l.lcode) > (select count(*)/2
                                  from locations
                                  where prov='Alberta')
except
select driver
from rides
where rdate < '2016-01-01';

.print Question 9 - drafiei
create view ride_info (rno, booked, available, rdate, price, src, dst) as
select r.rno, ifnull(sum(b.seats),0), r.seats-ifnull(sum(b.seats),0), rdate, 
       price, s.city, d.city
from rides r left outer join bookings b on r.rno=b.rno, locations s, locations d
where r.rdate > date ('now') and r.src=s.lcode and r.dst=d.lcode
group by r.rno, r.seats, rdate, price, s.city, d.city;

.print Question 10 - drafiei
select v.rno, v.booked, v.available, v.rdate, v.price, v.src, v.dst,
      r.driver, (strftime('%s','2019-01-01')-strftime('%s',v.rdate))/(60*60*24)
from ride_info v, rides r
where v.rno=r.rno and v.src='Edmonton' and v.dst='Calgary' and
      strftime('%Y', v.rdate)='2018' and
      strftime('%m', v.rdate)='12' and v.available>0
order by v.price desc;