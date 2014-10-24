class EventController < ApplicationController
  def index
    urls = %w[http://ohiounion.osu.edu/CentralCalendar/StudentLife.EventCalendar.Web.Service.RssHandler.ashx?d=11]
    feeds = Feedjira::Feed.fetch_and_parse urls

    feed = feeds["http://ohiounion.osu.edu/CentralCalendar/StudentLife.EventCalendar.Web.Service.RssHandler.ashx?d=11"]

    @title = feed.title
    @url = feed.url
    @entries = feed.entries
  end
end
