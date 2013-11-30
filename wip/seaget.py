#!/usr/bin/python2
# clean rewrite and combination of all my old python scripts
# TODO:
# - get basic functions []
# - add advances functions like:
#       looking for password at address $foo []
#       write to buffer/memory []
#       search for password without dumping []
#       add devices with known address []

import argparse
try:
    import serial
except:
    print 'You have to install pyserial'
    quit()
import sys,os,re,time

class SeaGet():
    debug=0
    timeout=0.005
    def send(self,command):
    #I'm not sure how to safely break this
    #I have added a ZeroCounter (zc) so that it won't run forever
        incom=[""]
        line=True
        self.ser.write(command+"\n")
        zc=0
        while line!="":
            try:
                line=self.ser.readline()
                line=self.ser.read(1000)
                incom.append(line)
            except:
                print 'Failed to read line.Maybe the timeout is too low'
                break
        incom="".join(incom)
        #You can (and have to) set different modi for the hd.
        #a different modus means you get a different set of commands
        #checking the modi after every command can be used for debugging and/or to verify that a command got executed correctly
        try:
            modus=re.findall('F3 (.)>',incom)
            modus=modus[len(modus)-1]
        except:
            print 'Failed to execute regex.This usually means that you didn\'t get the whole message or nothing at all'
            print 'Check your baud rate and timeout/zc'
            quit()
        return incom,modus

    def get_modus(self):
        return self.send("")[1]

    def set_baud(self,newbaud):
        modus=self.get_modus()
        print 'Setting baud to '+str(newbaud)
        if modus!="T":
            print 'Changing mode to T'
            self.send("/T")
        self.send("B"+str(newbaud))
        self.ser = serial.Serial(port=device, baudrate=newbaud, bytesize=8,parity='N',stopbits=1,timeout=self.timeout)
        newmodus=self.send("/"+modus)[1]
        if newmodus==modus:
            return True
        else:
            return False

    def __init__(self,baud, cont, dumptype, filename, device, new_baud):
        self.ser = serial.Serial(port=device, baudrate=baud, bytesize=8,parity='N',stopbits=1,timeout=self.timeout)
        #start diagnostic mode
        resp=self.send("\x1A")
        if resp[1]!="T" and resp[1]!="1":
            print "Something went probably wrong"
            print "Modus is "+resp[1]
            quit()
        #if you want a different baud rate you get it!
        if new_baud:
            self.set_baud(new_baud)
            baud=new_baud
        #set the right mode to access memory and buffer
        resp=self.send("/1")
        if resp[1]!="1":
            print 'Couldn\'t set modus to 1'
            print 'Failed with '+resp[0]
            if re.match('Input Command Error',resp[0]) and baud!=38400:
                print 'You probably set a higher baud rate, on a hd that has a bug'
                print 'Turn the hd off and on again and try the default baud rate 38400'
            quit()

    def read_buffer():
        pass
        
    def read_memory():
        pass

    def dump_buffer():
        pass
        
    def dump_memory():
        pass

def main():
    parser = argparse.ArgumentParser(description='Dump memory/buffer of a seagate hd using a serial connection.')
    parser.add_argument('--dumptype', metavar='memory/buffer', nargs=1, default='memory', help='What gets dumped')
    parser.add_argument('--baud', metavar=38400, default=38400, help='current baud rate [38400,115200]')
    parser.add_argument('--new-baud', metavar=115200, default=False, help='set new baud rate [38400,115200]')
    parser.add_argument('-c', dest='cont', action='store_const', const=True, help='Continue dump')
    parser.add_argument('--device', metavar='/dev/ttyUSB0', default='/dev/ttyUSB0', help='the serial device you use')
    parser.add_argument('filename', metavar='dumpfile', help='the name of the dump file, duh')
    args = parser.parse_args()
    see = SeaGet(args.baud, args.cont, args.dumptype, args.filename, args.device, args.new_baud)

if __name__ == '__main__':
    main()
