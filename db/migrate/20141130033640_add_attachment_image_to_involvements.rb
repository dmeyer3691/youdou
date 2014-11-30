class AddAttachmentImageToInvolvements < ActiveRecord::Migration
  def self.up
    change_table :involvements do |t|
      t.attachment :image
    end
  end

  def self.down
    remove_attachment :involvements, :image
  end
end
