class RemoveRankFromUsers < ActiveRecord::Migration
  def change
    remove_column :users, :rank, :string
  end
end
