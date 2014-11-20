class AddDoubleIndexToAnswerRelationships < ActiveRecord::Migration
  def change
  	add_index :answer_relationships, [:follower_id, :followed_id]
  end
end
