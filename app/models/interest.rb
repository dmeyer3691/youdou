class Interest < ActiveRecord::Base
  validates :name, presence: true
  validates :name, uniqueness: true

  acts_as_followable
end
