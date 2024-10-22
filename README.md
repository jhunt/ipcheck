ipcheck
=======

This is a silly flask app that exposes a single JSON endpoint,
`/check` that will return the country designation for the
requesting address based on data from the ipinfo.io data set
(which is freely available here:
 https://ipinfo.io/products/free-ip-database)

```sh
curl http://localhost:5000/check

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 29
Access-Control-Allow-Origin: \*
Connection: close

{"a":"68.94.112.198","l":"US"}
```

I use DuckDB to process the downloaded CSV file into something
that the application can more easily interrogate, by running this
query:

```sql
copy (
  select split_part(start_ip, '.', 1)::decimal as start_octet_1,
         split_part(start_ip, '.', 2)::decimal as start_octet_2,
         split_part(start_ip, '.', 3)::decimal as start_octet_3,
         split_part(start_ip, '.', 4)::decimal as start_octet_4,

         split_part(end_ip, '.', 1)::decimal as end_octet_1,
         split_part(end_ip, '.', 2)::decimal as end_octet_2,
         split_part(end_ip, '.', 3)::decimal as end_octet_3,
         split_part(end_ip, '.', 4)::decimal as end_octet_4,

         country,
    from read_csv('downloaded.csv'); -- don't forget to change!
   where start_ip like '%.%.%.%'
     and end_ip   like '%.%.%.%' -- only IPv4 for the moment
) into 'ipv4.csv';
```
