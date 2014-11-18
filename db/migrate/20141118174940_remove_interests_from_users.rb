class RemoveInterestsFromUsers < ActiveRecord::Migration
  def change
    remove_column :users, :interests, :string
  end
end
