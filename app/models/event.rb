class Event < ActiveRecord::Base
  scope :old, -> { where("date < ?", Date.today) }
end
