class AddAttributesToUsers < ActiveRecord::Migration
  def change
    add_column :users, :rank, :string
    add_column :users, :major, :string
    add_column :users, :minor, :string
    remove_column :users, :profile_id, :integer
  end
end
