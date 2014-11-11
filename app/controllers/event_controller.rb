class EventController < ApplicationController
  def index
    @events = Event.all.order('date ASC')

    if user_signed_in?
      @my_events = current_user.following_events
    end
  end
end
