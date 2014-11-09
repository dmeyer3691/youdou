require 'json'

class AnswerController < ApplicationController
	def index
		config_path = File.expand_path("../rpr.py", __FILE__)
		result = IO.popen("python3 #{config_path}")
		string = ""
		result.each do |line|
			string.concat(line)
		end

		@jsonData = JSON.parse(string)

		print @jsonData["title"]
	end
end
