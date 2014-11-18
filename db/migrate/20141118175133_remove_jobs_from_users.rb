class RemoveJobsFromUsers < ActiveRecord::Migration
  def change
    remove_column :users, :jobs, :string
  end
end
