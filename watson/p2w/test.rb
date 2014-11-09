require 'json'

@result = IO.popen("python3 rpr.py")
string = ""
@result.each do |line|
	string.concat(line)
end

jsonData = JSON.parse(string)

print jsonData["title"]