class ProfileController < ApplicationController
  RANK = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']

  def index
    unless user_signed_in?
      redirect_to root_path
    end

    @interest = Interest.new
    @involvement = Involvement.new

    @my_name = current_user.name.nil? ? current_user.email : current_user.name
    @my_interests = current_user.following_interests.order(:name)
    @my_involvements = current_user.following_involvements.order(:name)
    @my_events = current_user.following_events.current
  end

  def edit
  end

  def update
    @user = current_user

    if @user.update_attributes(user_params)
      redirect_to profile_path
    else
      redirect_to profile_path
    end
  end

  private

  def user_params
    params.require(:user).permit(:name, :avatar, :rank, :major, :minor)
  end
end
