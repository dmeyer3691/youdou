# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20141130220847) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "answer_relationships", force: true do |t|
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer  "follower_id"
    t.integer  "followed_id"
  end

  add_index "answer_relationships", ["followed_id"], name: "index_answer_relationships_on_followed_id", using: :btree
  add_index "answer_relationships", ["follower_id", "followed_id"], name: "index_answer_relationships_on_follower_id_and_followed_id", using: :btree
  add_index "answer_relationships", ["follower_id"], name: "index_answer_relationships_on_follower_id", using: :btree

  create_table "answers", force: true do |t|
    t.json     "answer"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "event_relationships", force: true do |t|
    t.integer  "follower_id"
    t.integer  "followed_id"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "event_relationships", ["followed_id"], name: "index_event_relationships_on_followed_id", using: :btree
  add_index "event_relationships", ["follower_id", "followed_id"], name: "index_event_relationships_on_follower_id_and_followed_id", unique: true, using: :btree
  add_index "event_relationships", ["follower_id"], name: "index_event_relationships_on_follower_id", using: :btree

  create_table "events", force: true do |t|
    t.string   "name"
    t.datetime "date"
    t.string   "url"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "follows", force: true do |t|
    t.integer  "followable_id",                   null: false
    t.string   "followable_type",                 null: false
    t.integer  "follower_id",                     null: false
    t.string   "follower_type",                   null: false
    t.boolean  "blocked",         default: false, null: false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "follows", ["followable_id", "followable_type"], name: "fk_followables", using: :btree
  add_index "follows", ["follower_id", "follower_type"], name: "fk_follows", using: :btree

  create_table "interests", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "image_file_name"
    t.string   "image_content_type"
    t.integer  "image_file_size"
    t.datetime "image_updated_at"
  end

  create_table "involvements", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "image_file_name"
    t.string   "image_content_type"
    t.integer  "image_file_size"
    t.datetime "image_updated_at"
  end

  create_table "profiles", force: true do |t|
    t.string   "username"
    t.string   "rank"
    t.string   "majors",      default: [], array: true
    t.string   "minors",      default: [], array: true
    t.string   "involvement", default: [], array: true
    t.string   "jobs",        default: [], array: true
    t.string   "interests",   default: [], array: true
    t.datetime "created_at"
    t.datetime "updated_at"
    t.integer  "user_id"
  end

  add_index "profiles", ["user_id"], name: "index_profiles_on_user_id", using: :btree

  create_table "recommendations", force: true do |t|
    t.string   "document"
    t.string   "title"
    t.text     "snippet"
    t.text     "content"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "recommendations_topics", id: false, force: true do |t|
    t.integer "recommendation_id"
    t.integer "topic_id"
  end

  create_table "topics", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "users", force: true do |t|
    t.string   "email",                  default: "", null: false
    t.string   "encrypted_password",     default: "", null: false
    t.string   "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer  "sign_in_count",          default: 0,  null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.string   "current_sign_in_ip"
    t.string   "last_sign_in_ip"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "provider"
    t.string   "uid"
    t.string   "name"
    t.string   "avatar_file_name"
    t.string   "avatar_content_type"
    t.integer  "avatar_file_size"
    t.datetime "avatar_updated_at"
    t.string   "rank"
    t.string   "major"
    t.string   "minor"
  end

  add_index "users", ["email"], name: "index_users_on_email", unique: true, using: :btree
  add_index "users", ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true, using: :btree

end
