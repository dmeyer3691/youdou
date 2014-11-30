Youdou::Application.routes.draw do
  get "question/index"
  get "academic/index"
  get "social/index"
  devise_for :users, :controllers => { :omniauth_callbacks => "users/omniauth_callbacks" }
  root 'home#index'

  get "about" => "about#index"
  get "events" => "event#index"
  get "feedback" => "about#feedback"
  get "licensing" => "about#licensing"
  get "answer" => "answer#index", :as => :answer
  get "question" => "question#index", :as => :question
  get "privacy" => "about#privacy"

  get "profile" => "profile#index", :as => :profile
  get "profile/edit" => "profile#edit", :as => :edit_profile
  patch 'profile/update', to: 'profile#update', as: :update_profile

  resources :event_relationships, only: [:create, :destroy]

  get 'interests/:interest_id/remove', to: 'interests#remove', as: 'remove_interest'
  resources :interests

  get 'involvements/:involvement_id/remove', to: 'involvements#remove', as: 'remove_involvement'
  resources :involvements

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products
  resources :answer, :only => [:show]
  resources :social, :only => [:show, :edit]
  resources :academic, :only => [:show, :edit]

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
