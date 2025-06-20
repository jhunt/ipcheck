ipcheck
=======

This is a silly flask app that exposes a single JSON endpoint,
`/check` that will return the country designation for the
requesting address based on data from the ipinfo.io data set
(which is freely available here: https://ipinfo.io/lite).
Specifically, download the JSON format, as `ipinfo_lite.json.gz`.

```sh
curl http://localhost:5000/check

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 29
Access-Control-Allow-Origin: \*
Connection: close

{"a":"68.94.112.198","l":"US","c":"US"}
```

Once the `ipinfo_lite.json.gz` file has been downloaded to the
root of the repository (for sizing reasons it does not get
committed) run the `./ingest` script to transform the JSON file
into a CSV file containing the bounds of each subnet range as
comparable columns.

Then, the `./materialize` script will import that into a SQLite3
database file (~470M) for performance reasons.  This database,
`ip.db` can be queried as follows:

```sh
$ ./ip2int 74.207.232.67
ipv4 74.207.232.67 1255139395

$ sqlite3 ip.db "select * from ip where '1255139395' between first_address and last_address"
US|NA|4|1255137280|1255145471|74.207.224.0/19|32|US
```

The `./ip2int` script loops over the IP address (v4 or v6) that
you pass to it, parses them, and then prints them as zero-padded
comparable string representations of the numeric address.
This is how we encode the boundaries for each subnet allocation in
the database, and is what makes the `BETWEEN` SQL operator work.

In the above example, the IPv4 address `74.207.232.67` is
converted to the integer 1255139395 as follows:

```
    74 x 2^24 =   1,241,513,984
 + 207 x 2^16 = +    13,565,952
 + 232 x 2^8  = +        59,392
 +  67 x 2^0  = +            67
                  1,255,139,395
```

Since this IP address is numerically expressed as 10 digits
already, the zero-padding is not evident.  Try `1.2.3.4`.
