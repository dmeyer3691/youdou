class AddIndexToAnswerRelationships < ActiveRecord::Migration
  def change
    add_index :answer_relationships, :followed_id
    add_index :answer_relationships, :follower_id
  end
end
