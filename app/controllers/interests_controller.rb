class InterestsController < ApplicationController
  def index
    @interests = Interest.all
  end

  def create
    @interest = Interest.find_or_create_by(interest_params)
    current_user.follow(@interest)

    redirect_to profile_path
  end

  def remove
    @interest = Interest.find(params[:interest_id])
    current_user.stop_following(@interest)
    redirect_to profile_path
  end

  private

  def interest_params
    params.require(:interest).permit(:name)
  end
end
