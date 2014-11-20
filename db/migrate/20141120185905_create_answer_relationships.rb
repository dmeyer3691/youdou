class CreateAnswerRelationships < ActiveRecord::Migration
  def change
    create_table :answer_relationships do |t|
      t.datetime :created_at
      t.datetime :updated_at
    end
  end
end
