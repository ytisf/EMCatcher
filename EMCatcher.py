#!/usr/bin/env python3

import os
import sys
import time
import json
import datetime
import argparse
import textwrap
import subprocess


LOGS_PATH = 'logs'
if not os.path.exists(LOGS_PATH):
	os.mkdir(LOGS_PATH)
CARDS_DUMP_PATH = 'cards'
if not os.path.exists(CARDS_DUMP_PATH):
	os.mkdir(CARDS_DUMP_PATH)



def dt_now():
	return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def load_settings(p='settings.conf'):
	set_json = json.loads(open(p).read())
	return set_json

def confirm_proxmark_binary(p='proxmark3'):
	p = subprocess.Popen(['which', p], stdout=subprocess.PIPE)
	p.wait()
	if p.returncode == 0:
		return p.stdout.read().decode('utf-8').strip()
	else:
		return False

def confirm_comport(comport):
	ap = subprocess.Popen(['proxmark3', '-c', 'help', comport], stdout=subprocess.PIPE)
	ap.wait()
	a = ap.stdout.read().decode('utf-8')
	if '[!] ERROR: invalid serial port ' in a:
		return False
	else:
		return True
	
def sample_input(dev, freq, custom_command=None):
	if custom_command:
		ap = subprocess.Popen(['proxmark3', '-c', custom_command, dev], stdout=subprocess.PIPE)

	else:
		ap = subprocess.Popen(['proxmark3', '-c', f'{freq} search', dev], stdout=subprocess.PIPE)

	ap.wait()
	a = ap.stdout.read().decode('utf-8')
	if 'No known 125/134 kHz tags found!' in a or 'No known/supported 13.56 MHz tags found' in a:
		return False
	else:
		n = str(int(time.time()))
		fn = os.path.join(CARDS_DUMP_PATH, n + '.lf')
		f = open(fn, 'w').write(a)
		return fn

def verify_settings(settings):
	if 'device' not in settings:
		sys.stdout.write("[!] No comport (device) specified\n")
		return False
	if 'freq' not in settings:
		sys.stdout.write("[!] No frequency (freq) specified\n")
		return False
	
	if settings['freq'] not in ['lf', 'hf']:
		sys.stdout.write("[!] Invalid frequency specified.\n")
		sys.stdout.write("[!] Valid frequencies: lf, hf.\n")
		return False

	if confirm_comport(comport=settings['device']) == False:
		sys.stdout.write(f"[!] Could not activate Proxmark on {settings['device']}.\n")
		return False

	return True

def help():
	sys.stdout.write("\nEMCatcher // Proxmark Headless Assistant\n")
	sys.stdout.write("Version: 0.1\n")
	sys.stdout.write("Author: tisf\n")
	sys.stdout.write("\n")
	sys.stdout.write("Usage: EMCatcher.py [options]\n")
	sys.stdout.write("\t-s\t--settings\t\t\tPath to settings file\n")
	sys.stdout.write("\t-v\t--verify_settings\t\tVerifies configurations file\n")
	sys.stdout.write("\t-h\t--help\t\t\t\tShow this help\n")
	sys.stdout.write("\n")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='EMCatcher', add_help=False)
	parser.add_argument('-s', '--settings', help='settings file', default='settings.conf')
	parser.add_argument('-v', '--verify_settings', help='verify settings file', action='store_true')
	parser.add_argument('-h', '--help', help='show help', action='store_true')
	args = parser.parse_args()

	if args.help:
		help()
		sys.exit(0)

	if args.verify_settings:
		if verify_settings(load_settings(args.settings)):
			sys.stdout.write("[+] Settings file verified.\n")
		else:
			sys.stdout.write("[!] Settings file failed verification.\n")
		sys.exit(0)

	LOG_LOCATION = f'{str(int(time.time()))}-collection_log.log'
	LOG_LOCATION = os.path.join(LOGS_PATH, LOG_LOCATION)
	logger = open(LOG_LOCATION, 'w')
	logger.write(f'{dt_now()} - Starting execution.\n')
	logger.flush()

	try:
		settings = load_settings()	
	except Exception as e:
		sys.stdout.write(f'{dt_now()} - Error loading settings file: {e}\n')
		logger.write(f'{dt_now()} - Error loading settings file: {e}\n')
		sys.exit(1)

	if not confirm_proxmark_binary():
		logger.write(f'{dt_now()} - Error: proxmark3 binary not found.\n')
		sys.stderr.write(f'{dt_now()} - Error: proxmark3 binary not found.\n')
		sys.exit(1)

	if confirm_comport(settings['device']):
		logger.write(f'{dt_now()} - Device \'{settings["device"]}\' found.\n')
		sys.stdout.write(f'{dt_now()} - Device \'{settings["device"]}\' found.\n')
	else:
		logger.write(f'{dt_now()} - Error: Device \'{settings["device"]}\' not found.\n')
		sys.stderr.write(f'{dt_now()} - Error: Device \'{settings["device"]}\' not found.\n')
		sys.exit(1)

	logger.write(f'{dt_now()} - Starting active collection.\n')
	sys.stdout.write(f'{dt_now()} - Starting active collection.\n')

	while True:
		logger.flush()
		try:
			time.sleep(settings['sample_rate'])
			if settings['custom_command']:
				if settings['custom_command'] != '':
					b = sample_input(settings['device'], settings['freq'], custom_command=settings['custom_command'])
				else:
					b = sample_input(settings['device'], settings['freq'])
			else:
				b = sample_input(settings['device'], settings['freq'])

			if b:
				logger.write(f'{dt_now()} - Sample collected!\n')
				sys.stdout.write(f'{dt_now()} - Sample collected!\n')

		except KeyboardInterrupt:
			logger.write(f'{dt_now()} - KeyboardInterrupt caught.\n')
			sys.stdout.write(f'\n{dt_now()} - KeyboardInterrupt caught.\n')
			sys.exit(0)

