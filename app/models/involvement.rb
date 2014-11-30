class Involvement < ActiveRecord::Base
  validates :name, presence: true
  validates :name, uniqueness: true

  before_save { |involvement| involvement.name = involvement.name.downcase }

  acts_as_followable

  # Paperclip
  has_attached_file :image, :styles => {
    :medium => "300x300#",
    :thumb => "100x100#"
  }, default_url: "http://placehold.it/300x300"
  validates_attachment_content_type :image, :content_type => /\Aimage\/.*\Z/
end
