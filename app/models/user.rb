class User < ActiveRecord::Base
  has_many :event_relationships, class_name: "EventRelationship",
    foreign_key: "follower_id", dependent: :destroy
  has_many :following_events, through: :event_relationships, source: :followed
  has_many :answer_relationships, class_name: "AnswerRelationship",
    foreign_key: "follower_id"
  has_many :saved_events, through: :answer_relationships, source: :followed
  has_one :profile

  acts_as_follower

  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  # :registerable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable,
         :omniauthable, :omniauth_providers => [:facebook]

  def self.from_omniauth(auth)
    where(provider: auth.provider, uid: auth.uid).first_or_create do |user|
      user.email = auth.info.email
      user.password = Devise.friendly_token[0,20]
      user.name = auth.info.name
      # user.image = auth.info.image # assuming the user model has an image
    end
  end

  # Paperclip
  has_attached_file :avatar, styles: {
    medium: "200x200#",
    thumb: "100x100#"
  }, default_url: "http://placehold.it/200x200"
  validates_attachment_content_type :avatar, :content_type => /\Aimage\/.*\Z/

  def self.new_with_session(params, session)
    super.tap do |user|
      if data = session["devise.facebook_data"] && session["devise.facebook_data"]["extra"]["raw_info"]
        user.email = data["email"] if user.email.blank?
      end
    end
  end

  def follow_event(event)
    event_relationships.create(followed_id: event.id)
  end

  def unfollow_event(event)
    event_relationships.find_by(followed_id: event.id).destroy
  end

  def following_event?(event)
    following_events.include?(event)
  end
end
