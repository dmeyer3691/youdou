class AddMinorsToUser < ActiveRecord::Migration
  def change
    add_column :users, :minors, :string, array: true, default: '{}'
  end
end
