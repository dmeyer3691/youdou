class AddJobsToUser < ActiveRecord::Migration
  def change
    add_column :users, :jobs, :string, array: true, default: '{}'
  end
end
