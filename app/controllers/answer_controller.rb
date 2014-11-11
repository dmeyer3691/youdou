require 'json'

class AnswerController < ApplicationController
	def index

		query = params['query']
		config_path = File.expand_path("../rpr.py", __FILE__)
		result = IO.popen("python3 #{config_path} \"" + query + "\"")
		string = ""
		result.each do |line|
			string.concat(line)
		end

		@jsonData = JSON.parse(string)
		@recommended = @jsonData["results"]["recommended"]
		@possible = @jsonData["results"]["possible"]
		@other = @jsonData["results"]["other"]
		@events = @jsonData["events"]
		print :query
	end
end
