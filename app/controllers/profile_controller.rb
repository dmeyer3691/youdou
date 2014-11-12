class ProfileController < ApplicationController
  def index
    unless user_signed_in?
      redirect_to root_path
    end

    @my_events = current_user.following_events.current
  end

  def edit
  end
end
