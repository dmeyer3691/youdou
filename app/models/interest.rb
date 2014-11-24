class Interest < ActiveRecord::Base
  validates :name, presence: true
  validates :name, uniqueness: true

  before_save { |interest| interest.name = interest.name.downcase }

  acts_as_followable
end
