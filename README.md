# Virtual Server (Python)

## Summary

This is implementation VServer used python. The source project [Nodejs-VServer](https://github.com/alphatan/nodejs-vserver).

Base on Python2.7 and Flask 0.10.1, you can refers ```requirements.txt``` .

Virtual Server (vserver) is used as a virtual https server for test
purpose.

It behaves according to the request's headers.

For example, it can be controlled to return 404 by setting the header
'X-VS-CTRL-Status-Code: 404'.

For more details, please refers to the section [HTTP HEADER Parameters](#http-header-parameters).

## Quick Start

1. Generate self-signed certs for vserver by openssl.

	Generate vserver certs:

	```bash
	$ openssl req -x509 -sha256 -passout "pass:nu5/SM/JIRHa=pi8" -days 365 -newkey rsa:2048 -keyout vserver.pri.pem -out vserver.crt.pem
	```

	Put them into the 'certs' directory.

2. Generate self-signed certs for vserver-client by openssl

	Generate vserver-client certs:

	```bash
	$ openssl req -x509 -sha256 -passout "pass:P9Va6!" -days 365 -newkey rsa:2048 -keyout vserver-client.pri.pem -out vserver-client.crt.pem
	```

	Put them into the 'certs' directory.


3. Specify trusted client certs to the 'TRUSTED_CACERT' variable in file '**config.py**'.

	```bash
	SERVER_SSL_CERT = 'certs/vserver.crt.pem'
	SERVER_SSL_KEY = 'certs/vserver.pri.pem'
	SERVER_SSL_PASS = 'nu5/SM/JIRHa=pi8'
	TRUSTED_CACERT = 'certs/vserver-client.crt.pem'
	```

	See [Client Certs](#client-certs) for details.

4. Start server.

	```bash
	$ python vserver.py
	```

5. Test with curl

	Test certs:

	```bash
	$ curl -i -X POST -d "{ \"key\": \"value\" }" --cert certs/vserver-client.crt.pem  --key certs/vserver-client.pri.pem --pass P9Va6! --cacert certs/vserver.crt.pem  -H "X-VS-CTRL-STATUS-CODE: 404" -H "CONTENT-TYPE: text/json; charset=utf8" --insecure https://127.0.0.1:8443
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
	                                 Dload  Upload   Total   Spent    Left  Speed
	100    22  100    11  100    11     63     63 --:--:-- --:--:-- --:--:--    63
	HTTP/1.0 404 NOT FOUND
	Content-Type: text/json; charset=utf8
	Content-Length: 18
	Server: Werkzeug/0.11.3 Python/2.7.11
	Date: Tue, 29 Mar 2016 01:29:32 GMT

	{ "key": "value" }
	```

	Specify the response status code:

	```bash
	$ curl -i --cert certs/vserver-client.crt.pem --key certs/vserver-client.pri.pem --pass P9Va6! --cacert certs/vserver.crt.pem --insecure -H "x-vs-ctrl-status-code: 404" -H "Content-Type: text/json; charset=utf8" -d "{ \"key\": \"value\" }" -X POST https://127.0.0.1:8443
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
	                                 Dload  Upload   Total   Spent    Left  Speed
	100    36  100    18  100    18    104    104 --:--:-- --:--:-- --:--:--   104
	HTTP/1.0 404 NOT FOUND
	Content-Type: text/json; charset=utf8
	Content-Length: 18
	Server: Werkzeug/0.11.3 Python/2.7.11
	Date: Tue, 29 Mar 2016 01:31:57 GMT

	{ "key": "value" }

	```

	Wait 5 seconds then return empty body with 404 status code:	
	```bash
	$ curl -i --cert certs/vserver-client.crt.pem --key certs/vserver-client.pri.pem --pass P9Va6! --cacert certs/vserver.crt.pem --insecure -H "x-vs-ctrl-body-content-length: 0" -H "x-vs-ctrl-response-interval: 5" -H "x-vs-ctrl-status-code: 404" -H "Content-Type: text/json; charset=utf8" -d "{ \"key\": \"value\" }" -X POST https://127.0.0.1:8443
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
	                                 Dload  Upload   Total   Spent    Left  Speed
	100    18    0     0  100    18      0      3  0:00:06  0:00:05  0:00:01     0
	HTTP/1.0 404 NOT FOUND
	Content-Type: text/json; charset=utf8
	Content-Length: 0
	Server: Werkzeug/0.11.3 Python/2.7.11
	Date: Tue, 29 Mar 2016 01:33:36 GMT

	```


## HTTP HEADER Parameters

### X-VS-CTRL-Status-Code: 2xx, 3xx, 4xx, 5xx

Define the return status code. The default value is: 200.

### X-VS-CTRL-Header-isClean: true|false

Define whether to clean all headers. Or it will return
all headers in the request by default.

	true: clean all headers from the request
	false: keep the same headers as in the request (except the ones defined in "FILTER_HEADERS" of config.py)

### X-VS-CTRL-Body-Content-isRandom: true|false

Define whether generate random content, the header '**Content-Type:
text/plain;charset=utf8**' will be set to the response.

	true: generate randome content.
	false: use the original content. (default)

### X-VS-CTRL-Body-Content-Length: N|Nk|Nm

Define the content length.

	-1: return the body content in the request. (default)
	N|Nk|Nm:  define the content length.

N is a number, states bytes of the content. e.g. "1024", "1k", "1m"

If the content of the request is not enough for this requirement, the
content will be repeated. If the content of the request is too long,
it will be truncated.

### X-VS-CTRL-Response-Interval: N(seconds)

Define the waiting time before return.

	-1: return immediately (default)
	N: wait (at least) N seconds before returning.


## Client Certs

By default, vserver requires client cert to validate requests. All configurations can be set in the file '**config.py**'.

1. Specify your own certs in the "TRUSTED_CACERT" property.

	Example:

	```bash
	TRUSTED_CACERT = 'certs/vserver-client.crt.pem'
	```

2. Accept client connections without trusted certs, this is Fixed inside the code of vserver.py

	```bash 
		ssl_ctx.verify_mode = ssl.CERT_REQUIRED
	```

## License

`python-vserver` is licensed under GPL v3. The license is
availabe [here](/LICENSE).

	


