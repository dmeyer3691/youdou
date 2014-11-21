desc "This task is called by the Heroku scheduler add-on"
task :delete_old_events => :environment do
  puts "Deleting old events..."
  EventWorker.delete_old_events
  puts "done."
end

task :update_union_events => :environment do
  puts "Updating events..."
  EventWorker.update_union_events
  puts "done."
end

task :update_ecs_events => :environment do
  puts "Updating events..."
  EventWorker.update_ecs_events
  puts "done."
end

# task :send_reminders => :environment do
  # User.send_reminders
# end

