require "rails_helper"

RSpec.describe Interest, :type => :model do
  it { should validate_presence_of(:name) }
  it { should validate_uniqueness_of(:name) }

  it "should not be case sensitive" do
    anime = Interest.create!(name: "Anime")

    expect(anime.name).to eq("anime")
  end
end
