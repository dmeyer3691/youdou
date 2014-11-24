class ProfileController < ApplicationController
  def index
    unless user_signed_in?
      redirect_to root_path
    end

    @interest = Interest.new

    @name = current_user.name

    @my_interests = current_user.following_interests.order(:name)
    @my_events = current_user.following_events.current
  end

  def edit
  	@name = current_user.name
  end

  def update_name
  	@name = params[:name]
  	current_user.name = @name

  	render 'edit'
  end
end
