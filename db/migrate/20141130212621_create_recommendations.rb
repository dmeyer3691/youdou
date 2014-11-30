class CreateRecommendations < ActiveRecord::Migration
  def change
    create_table :recommendations do |t|
      t.string :document
      t.string :title
      t.text :snippet
      t.text :content

      t.timestamps
    end
  end
end
