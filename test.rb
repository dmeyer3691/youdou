require 'open-uri'
require 'nokogiri'

doc = Nokogiri::HTML(open("http://ohiounion.osu.edu/events.aspx/2014/11/6/39234/beanie-drake-scholarship-application"))

puts doc.css(".date")[0].text
