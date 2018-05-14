#!/usr/bin/python
# -*- coding: UTF-8 -*-
import configparser

class Config(object):
	def __init__(self, file_adress = 'spider.conf'):
		cp = configparser.SafeConfigParser()
		cp.read(file_adress)
		self.cp = cp
		self.file_adress = file_adress

	def get_config(self, key):
		return self.cp.get('spider', key)

	def set_config(self, key, value):
		self.cp.set('spider', key, value)
		cp.write(open(self.file_adress, 'w'))
		cp.write(sys.stdout)

if  __name__ == '__main__':
	config = Config()
	print('all sections:'+str(config.cp.sections))