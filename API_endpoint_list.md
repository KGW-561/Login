# SCVs API Endpoint list

| **Controller**          | **Endpoint**                                  | **HTTP Method** | **Description**                                  |
|--------------------------|-----------------------------------------------|----------------|--------------------------------------------------|
| BaseController           | /                                             | GET            | Main page with indices, forex data, and news     |
| UserController           | /accountdelsuccess                           | GET            | Display account deletion success page            |
| CommunityController      | /addComment                                  | POST           | Add a comment to a community                     |
| AdminController          | /admin/deleteUserList                        | POST           | Delete selected users                            |
| AdminController          | /admin/userList                              | GET            | Get user list with filters and pagination        |
| AdminController          | /admin/userList                              | POST           | Get filtered user list with search input         |
| UserController           | /api/check-email                             | POST           | Check if email is duplicate                      |
| UserController           | /api/check-nickname                          | POST           | Check if nickname is duplicate                   |
| UserController           | /api/check-password                          | POST           | Check if password is duplicate                   |
| CommunityController      | /castVote                                    | POST           | Cast a vote in a community                       |
| CommunityController      | /community                                   | GET            | Get community details for a ticker               |
| CommunityController      | /deleteComment                               | POST           | Delete a comment                                 |
| CommunityController      | /editComment                                 | POST           | Edit a comment                                   |
| CustomErrorController    | /error                                       | GET            | Handle errors and return appropriate error pages |
| KorController            | /kor                                         | GET            | Get list of Korean news with pagination          |
| KorController            | /kor/{korEconNewsId}                         | GET            | Get detailed Korean news by ID                   |
| UserController           | /login                                       | GET            | Display login page                               |
| ProxyController          | /proxy/fetch                                 | GET            | Fetch data from an external API via proxy        |
| PSAController            | /PSA-add                                     | GET            | View page to add a new PSA                       |
| PSAController            | /PSA-add                                     | POST           | Add a new PSA                                    |
| PSAController            | /PSA-detail/{id}                             | GET            | Get detailed PSA by ID                           |
| PSAController            | /PSA-list                                    | GET            | Get a list of PSAs with optional search          |
| PSAController            | /PSA/delete/{id}                             | GET            | Delete a PSA                                     |
| PSAController            | /PSA/update/{id}                             | GET            | View page to update a PSA                        |
| PSAController            | /PSA/update/{id}                             | POST           | Update a PSA                                     |
| UserController           | /signup                                      | GET            | Display signup page                              |
| UserController           | /signup                                      | POST           | Register a new user                              |
| UserController           | /signupSuccess                               | GET            | Display signup success page                      |
| StockWatchController     | /stocknews/{tickerId}/{stockNewsId}          | GET            | Get detailed stock news by ID                    |
| StockWatchController     | /stockwatch                                  | GET            | Get stock watch details for a ticker             |
| UsaController            | /usa                                         | GET            | Get list of USA news with pagination             |
| UsaController            | /usa/{usaEconNewsId}                         | GET            | Get detailed USA news by ID                      |
| UserController           | /user/accountdel                             | GET            | Display account deletion page                    |
| UserController           | /user/accountdel                             | POST           | Delete user account                              |
| UserController           | /user/passwordchange                         | GET            | Display password change page                     |
| UserController           | /user/passwordcheck                          | GET            | Display password check page                      |
| UserController           | /user/profile                                | GET            | Display user profile page                        |
| UserController           | /user/update                                 | POST           | Update user information                          |
| WatchlistController      | /watchlist                                   | GET            | View user's watchlist                            |
| WatchlistController      | /watchlist/add                               | POST           | Add a stock to the user's watchlist              |
| WatchlistController      | /watchlist/delete                            | POST           | Delete a stock from the user's watchlist         |
