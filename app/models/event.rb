class Event < ActiveRecord::Base
  scope :old, -> { where("date < ?", Date.today) }
  scope :current, -> { where("date >= ?", Date.today) }

  has_many :event_relationships, class_name: "EventRelationship",
    foreign_key: "followed_id", dependent: :destroy

  paginates_per 10
end
