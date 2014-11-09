class EventController < ApplicationController
  def index
    @events = Event.all
  end
end
