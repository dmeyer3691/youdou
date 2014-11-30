class InvolvementsController < ApplicationController
  def create
    @involvement = Involvement.find_or_create_by(involvement_params)
    current_user.follow(@involvement)

    redirect_to profile_path
  end

  def remove
    @involvement = Involvement.find(params[:involvement_id])
    current_user.stop_following(@involvement)
    redirect_to profile_path
  end

  private

  def involvement_params
    params.require(:involvement).permit(:name)
  end
end

