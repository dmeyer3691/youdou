class RemoveInvolvementFromUsers < ActiveRecord::Migration
  def change
    remove_column :users, :involvement, :string
  end
end
