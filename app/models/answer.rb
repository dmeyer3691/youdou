class Answer < ActiveRecord::Base
	has_many :answer_relationships, class_name: "AnswerRelationship",
    foreign_key: "followed_id"
end
