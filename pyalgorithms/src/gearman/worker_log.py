#coding=utf-8
'''
Created on 2012-8-12

@author: fengclient
'''

import cPickle
import logging
import logging.handlers
import SocketServer
import struct
import config

logger=logging.getLogger(config.logger_name)
logger.setLevel(logging.DEBUG)
fh=logging.FileHandler(config.log_filename)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    '''
    copied from http://docs.python.org/release/2.6.8/library/logging.html#sending-and-receiving-logging-events-across-a-network
    '''

    def handle(self):
        while True:
            chunk=self.connection.recv(4)
            if len(chunk)<4:
                break
            slen=struct.unpack(">L",chunk)[0]
            chunk=self.connection.recv(slen)
            while len(chunk)<slen:
                chunk=chunk+self.connection.recv(slen-len(chunk))
            obj=self.unPickle(chunk)
            record=logging.makeLogRecord(obj)
            self.handleLogRecord(record)
    
    def unPickle(self,data):
        return cPickle.loads(data)
    
    def handleLogRecord(self,record):
        name=self.server.logname if self.server.logname else record.name
        logger=logging.getLogger(name)
        logger.handle(record)
        
class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
    """simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

def main():
    logging.basicConfig(
        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
    tcpserver = LogRecordSocketReceiver(config.logging_host,config.logging_port)
    print 'About to start TCP server...'
    tcpserver.serve_until_stopped()

if __name__ == '__main__':
    main()
