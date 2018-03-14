# -*- coding:utf-8 -*-
#!/usr/bin/env python3
import xml.etree.ElementTree as ET

def parse_xml(data):
	if len(data) == 0:
		return None
	xml_data = ET.fromstring(data)
	msg_type = xml_data.find('MsgType').text
	if msg_type == 'text':
		return Text_msg(xml_data)
	elif msg_type == 'image':
		return Image_msg(xml_data)
	elif msg_type == 'voice':
		return Voice_msg(xml_data)
	elif msg_type == 'video':
		return Video_msg(xml_data)
	elif msg_type == 'shortvideo':
		return Shortvideo_msg(xml_data)
	elif msg_type == 'location':
		return Location_msg(xml_data)
	elif msg_type == 'link':
		return Link_msg(xml_data)

class Msg(object):
    def __init__(self, xml_data):
        self.to_user_name = xml_data.find('ToUserName').text
        self.from_user_name = xml_data.find('FromUserName').text
        self.create_time = xml_data.find('CreateTime').text
        self.msg_type = xml_data.find('MsgType').text
        self.msg_id = xml_data.find('MsgId').text

class Text_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.msg_type = xml_data.find('MsgType').text
        self.Content = xml_data.find('Content').text.encode("utf-8")

class Image_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)

class Voice_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)

class Video_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)

class Shortvideo_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)

class Location_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)

class Link_msg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
