class CreateTopicsAndAssociationWithRecommendations < ActiveRecord::Migration
  def change
    create_table :topics do |t|
      t.string :name
      t.timestamps
    end

    create_table :recommendations_topics, id: false do |t|
      t.belongs_to :recommendation
      t.belongs_to :topic
    end
  end
end
