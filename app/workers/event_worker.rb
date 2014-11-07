# app/workers/event_worker.rb
class EventWorker
  include Sidekiq::Worker

  def self.update_events
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
end
