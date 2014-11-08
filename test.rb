require 'open-uri'
require 'nokogiri'

doc = Nokogiri::HTML(open("http://ohiounion.osu.edu/events.aspx/2014/11/7/39546/deadline-to-register-for-buckeyethon-2015"))

categoryLinks = doc.css("div.sidebar a")
keywords = []
for category in categoryLinks do 
	keywords.push(category.text)

end

