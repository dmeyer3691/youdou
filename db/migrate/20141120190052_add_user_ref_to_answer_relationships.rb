class AddUserRefToAnswerRelationships < ActiveRecord::Migration
  def change
    add_column :answer_relationships, :follower_id, :integer
    add_column :answer_relationships, :followed_id, :integer
  end
end
