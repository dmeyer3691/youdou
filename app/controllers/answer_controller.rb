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
		if (@jsonData)
			@results = @jsonData["results"]
			if (@results)
				recommended = @jsonData["results"]["recommended"]
				@possible = @jsonData["results"]["possible"]
				@other = @jsonData["results"]["other"]
				@events = @jsonData["events"]
				@offers = @jsonData["offers"]
				print :query
			else
				recommended = []
				@possible = []
				@other = []
				@events = []
				@offers = []
			end
		end

    @recommendations = []

    recommended.each do |recommendation|
      new_recommendation = Recommendation.where(
        document: recommendation["document"],
        title: recommendation["title"],
        snippet: recommendation["snippet"],
        content: recommendation["content"]
      ).first_or_create

      if new_recommendation.topics.empty?
        recommendation["relevantTo"].each do |topic|
          new_topic = Topic.where(name: topic).first_or_create

          new_recommendation.topics << new_topic
        end
      end

      @recommendations << new_recommendation
    end
	end

  def save
    @recommendation = Recommendation.find(params[:recommendation_id])
    current_user.follow(@recommendation)

    respond_to do |format|
      format.html { redirect_to profile_path }
      format.js
    end
  end

  def unsave
    @recommendation = Recommendation.find(params[:recommendation_id])
    current_user.stop_following(@recommendation)

    respond_to do |format|
      format.html { redirect_to profile_path }
      format.js
    end
  end

end
