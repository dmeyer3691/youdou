class EventController < ApplicationController
  def index
    @events = Event.all

    if user_signed_in?
      @my_events = current_user.following_events
    end
  end
end
