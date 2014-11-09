class CreateEventRelationships < ActiveRecord::Migration
  def change
    create_table :event_relationships do |t|
      t.integer :follower_id
      t.integer :followed_id

      t.timestamps
    end

    add_index :event_relationships, :follower_id
    add_index :event_relationships, :followed_id
    add_index :event_relationships, [:follower_id, :followed_id], unique: true
  end
end
