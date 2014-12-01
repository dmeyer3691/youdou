class Recommendation < ActiveRecord::Base
  acts_as_followable

  has_and_belongs_to_many :topics
end
