class AddInterestsToUser < ActiveRecord::Migration
  def change
    add_column :users, :interests, :string, array: true, default: '{}'
  end
end
