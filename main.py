import subprocess
from workflow import Workflow
import sys
reload(sys)  
sys.setdefaultencoding('utf8') 

def getConnections():
    script = '''
        tell application "CloudMounter"
            tell connections
                return {name, Kind, email, isMounted}
            end tell
        end tell
        '''

    proc = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    stdout_output = proc.communicate(script.encode())[0]
    return stdout_output.decode().split(',')

def main(wf):
    flag = wf.args[0]
    query = wf.args[1]
    log.debug('flag : %r', flag)
    log.debug('query : %r', query)
    if(flag == "list-m"):
        itemList = listConnections()
        log.debug('itemList: %r', itemList)
        for item in itemList:
            if(query!=""):
                if(query.upper() not in item[0].upper()):
                    continue
            if(correctStr(item[3])=="true"):
                continue
            wf.add_item(title=item[0],
                        arg=item[0],
                        subtitle="press 'Enter' to mount",
                        icon ="./icons/"+correctStr(item[1])+".icns",
                        valid = True)
    elif(flag == "list-u"):
        itemList = listConnections()
        log.debug('itemList: %r', itemList)
        for item in itemList:
            if(query!=""):
                if(query.upper() not in item[0].upper()):
                    continue
            if(correctStr(item[3])=="false"):
                continue
            wf.add_item(title=item[0],
                        arg=item[0],
                        subtitle="press 'Enter' to unmount",
                        icon ="./icons/"+correctStr(item[1])+".icns",
                        valid = True)
    elif(flag == "mount"):
        mount(query.decode())
    elif(flag == "unmount"):
        unmount(query.decode())
    
    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()

def correctStr(s):
    return (s.strip('\n')).strip()

def listConnections():
    connections = getConnections()
    itemLen = len(connections)/4;
    itemList = []
    for index in range(itemLen):
        connections[index] = connections[index].strip('\n')
        connections[index] = connections[index].strip()
        itemList.append((connections[index],connections[index+itemLen],connections[index+2*itemLen],connections[index+3*itemLen]))
    return sorted(itemList,key=lambda s: s[0])
    

def mount(connection):
    script = '''
    tell application "CloudMounter"
        mount connection "''' +correctStr(connection) + '''"
    end tell'''
    log.debug('script: %r', script )
    proc = subprocess.Popen(['osascript', '-'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
    stdout_output = proc.communicate(script.encode())[0]

def unmount(connection):
    script = '''
    tell application "CloudMounter"
        unmount connection "''' +correctStr(connection) + '''"
    end tell'''
    log.debug('script: %r', script )
    proc = subprocess.Popen(['osascript', '-'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
    stdout_output = proc.communicate(script.encode())[0]

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))