class RemoveMajorsFromUsers < ActiveRecord::Migration
  def change
    remove_column :users, :majors, :string
  end
end
