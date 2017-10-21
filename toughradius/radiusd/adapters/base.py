#!/usr/bin/env python
#coding:utf-8

from toughradius.txradius.radius import dictionary
from toughradius.radiusd.radutils import parse_auth_packet
from toughradius.radiusd.radutils import parse_acct_packet
from toughradius.radiusd.radutils import process_auth_reply
from toughradius.radiusd.radutils import process_acct_reply
import gevent
import logging

class BasicAdapter(object):

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.dictionary = dictionary.Dictionary(config.radiusd.dictionary)

    def get_clients(self):
        return {}

    def handleAuth(self,socket, data, address):
        try:
            req = parse_auth_packet(data,address,self.config.vendors,self.get_clients(),self.dictionary)
            prereply = self.auth(req)
            reply = process_auth_reply(req, prereply)
            gevent.spawn(socket.sendto,reply.ReplyPacket(),address)
        except:
            self.logger.error( "Handle Radius Auth error",exc_info=True)

    def handleAcct(self,socket, data, address):
        try:
            req = parse_acct_packet(data,address,self.config.vendors,self.get_clients(),self.dictionary)
            prereply = self.acct(req)
            reply = process_acct_reply(req, prereply)
            gevent.spawn(socket.sendto, reply.ReplyPacket(), address)
        except:
            self.logger.error("Handle Radius Acct error",exc_info=True)




