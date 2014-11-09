class User < ActiveRecord::Base
  has_many :event_relationships, class_name: "EventRelationship",
    foreign_key: "follower_id", dependent: :destroy
  has_many :following_events, through: :event_relationships, source: :followed

  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable,
         :omniauthable, :omniauth_providers => [:facebook]

  def self.from_omniauth(auth)
    where(provider: auth.provider, uid: auth.uid).first_or_create do |user|
      user.email = auth.info.email
      user.password = Devise.friendly_token[0,20]
      # user.name = auth.info.name   # assuming the user model has a name
      # user.image = auth.info.image # assuming the user model has an image
    end
  end

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
