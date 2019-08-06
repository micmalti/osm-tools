#! /usr/bin/python3

# Author: Michael Gauci

import argparse
import requests
import json

def overpass_query(area_code, admin_level):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query =  """[out:json][timeout:300];
                area["ISO3166-2"~"{0}"]->.searchArea;
                (
                    rel["admin_level"="{1}"](area.searchArea);
                );
                out body;
                >;
                out skel qt;""".format(area_code, admin_level)
    response = requests.get(overpass_url, params={'data': query})
    return response.json()

def run(args):
    area_code = args.code
    admin_level = args.level
    output_file = args.output
    data = overpass_query(area_code,admin_level)
    i = 0
    with open(output_file, 'w+') as f:
        while True:
            if "tags" in data["elements"][i]:
                f.write(data["elements"][i]["tags"]["name"])
                f.write('\n')
                i += 1
            else:
                break

def main():
	parser=argparse.ArgumentParser(description="Retrieves all the city names within the region of interest")
	parser.add_argument("-c",help="Area code (check out ISO3166-2.csv)", dest="code", type=str, required=True)
	parser.add_argument("-l",help="OSM administrative boundary level", dest="level", type=str, default="8")
	parser.add_argument("-out", help="Output file name", dest="output", type=str, default="city_list.txt")
	parser.set_defaults(func=run)
	args=parser.parse_args()
	args.func(args)

if __name__ == '__main__':
    main()
