require 'json'

class AnswerRelationshipController < ApplicationController
  def create
    answer = Answer.find(params[:followed_id])
    current_user.save_answer(answer)
    redirect_to answer_path
  end

  def destroy
    answer = AnswerRelationship.find(params[:id]).followed
    current_user.forget_answer(answer)
    redirect_to answer_path
  end
end
