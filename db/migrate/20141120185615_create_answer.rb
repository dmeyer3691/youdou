class CreateAnswer < ActiveRecord::Migration
  def change
    create_table :answers do |t|
      t.json :answer
    end
  end
end
