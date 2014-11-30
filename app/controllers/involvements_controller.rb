class InvolvementsController < ApplicationController
  def index
    @involvements = Involvement.all
  end

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

  def update
    @involvement = Involvement.find(params[:id])

    if @involvement.update_attributes(involvement_params)
      redirect_to involvements_path
    else
      redirect_to involvements_path
    end
  end

  private

  def involvement_params
    params.require(:involvement).permit(:name, :image)
  end
end

