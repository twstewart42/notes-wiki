#!/usr/bin/python
import pygeoip
import argparse
gi = pygeoip.GeoIP('GeoLiteCity.dat')
def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['region_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print '[*] Target: ' + tgt + ' Geo-located. '
    print '[+] '+str(city)+', '+str(region)+', '+str(country)
    print '[+] Latitude: '+str(lat)+', Longitude: '+str(long)

def main():
   parser = argparse.ArgumentParser(description='finds geolocation of an IP address')
   parser.add_argument('ipaddr', metavar='I', nargs='+', type=str, help='8.8.8.8')
   args = parser.parse_args()
   tgts = args.ipaddr
   for tgt in tgts:
       printRecord(tgt)

if __name__ == '__main__':
    main()
