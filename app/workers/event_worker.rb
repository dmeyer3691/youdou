# app/workers/event_worker.rb
require 'open-uri'
class EventWorker
  include Sidekiq::Worker

  def self.delete_old_events
    Event.old.delete_all
  end

  def self.update_union_events
    urls = %w[http://ohiounion.osu.edu/CentralCalendar/StudentLife.EventCalendar.Web.Service.RssHandler.ashx?d=11]
    feeds = Feedjira::Feed.fetch_and_parse urls
    feed = feeds["http://ohiounion.osu.edu/CentralCalendar/StudentLife.EventCalendar.Web.Service.RssHandler.ashx?d=11"]

    feed.entries.each do |entry|
      url = entry.url
      doc = Nokogiri::HTML(open(url))
      name = entry.title
      date = Date.parse(doc.css(".date")[0].text)

      if (Event.where(name: name, date: date).empty?)
        Event.create(name: name, date: date, url: url)
      end
    end
  end

  def self.update_ecs_events
    doc = Nokogiri::HTML(open("https://ecs.osu.edu/events"))
    events_dirty = doc.css(".osu-events-list .osu-widget-article")

    events_dirty.each do |event|
      url = "https://ecs.osu.edu" + event.css(".osu-title a").first["href"]
      name = event.css(".osu-title").text
      date = Date.parse event.css(".osu-events-date").text

      if Event.where(name: name, date: date).empty?
        Event.create(name: name, date: date, url: url)
      end
    end
  end
end
