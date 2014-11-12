class EventController < ApplicationController
  before_action :authenticate_user!

  def index
    @events = Event.current.order('date ASC').page params[:page]

    if user_signed_in?
      @my_events = current_user.following_events.current.order('date ASC')
    end
  end
end
