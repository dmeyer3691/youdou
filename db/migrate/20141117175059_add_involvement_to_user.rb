class AddInvolvementToUser < ActiveRecord::Migration
  def change
    add_column :users, :involvement, :string, array: true, default: '{}'
  end
end
