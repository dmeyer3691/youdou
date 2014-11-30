class AddImagesToInterests < ActiveRecord::Migration
  def self.up
    add_attachment :interests, :image
  end

  def self.down
    remove_attachment :interests, :image
  end
end
