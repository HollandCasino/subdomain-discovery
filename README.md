# subscan
Simple Python script to uncover both active and expired subdomains that also checks the response code.
The script uses https://crt.sh/ to discover subdomains and returns the status code for each discovered subdomain. The output will always show "200" first, and "-1" represents an error.
