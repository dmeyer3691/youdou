class CreateProfiles < ActiveRecord::Migration
  def change
    create_table :profiles do |t|
      t.string :username
      t.string :rank
      t.string :majors, array: true, default: []
      t.string :minors, array: true, default: []
      t.string :involvement, array: true, default: []
      t.string :jobs, array: true, default: []
      t.string :interests, array: true, default: []
    end
  end
end
