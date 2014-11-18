class RemoveMinorsFromUsers < ActiveRecord::Migration
  def change
    remove_column :users, :minors, :string
  end
end
