class ProfileController < ApplicationController
  def index
    unless user_signed_in?
      redirect_to root_path
    end
  end

  def edit
  end
end
