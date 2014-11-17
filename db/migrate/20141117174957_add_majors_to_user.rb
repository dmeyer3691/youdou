class AddMajorsToUser < ActiveRecord::Migration
  def change
    add_column :users, :majors, :string, array: true, default: '{}'
  end
end
