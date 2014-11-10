desc "This task is called by the Heroku scheduler add-on"
task :update_events => :environment do
  puts "Updating events..."
  EventWorker.update_events
  puts "done."
end

task :delete_old_events => :environment do
  puts "Deleting old events..."
  Event.old.delete_all
  puts "done."
end

# task :send_reminders => :environment do
  # User.send_reminders
# end

