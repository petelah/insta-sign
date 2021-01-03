## Discuss how the application will handle the privacy of user data within the system, and how security features of the frameworks you are utilising will assist to mitigate security concerns.


SQL Alchemy mitigates the risk of dealing with the threat of SQL injection attack by sanitising data input and output to and from the user. 
It essentially sits there as a gatekeeper or firewall for the data.

By sanitising and validating the data before it gets to the database the risk of a threat actor sending an injection attack is very low.

We also place the database behind a private subnet so the api gateway machine is the only input and output to the database. 
This allows up to control the flow of data through the ORM with sanitization and validation as stated above and it also makes 
sure that no outside users can access the naked machine and potentially exploit a different vulnerability and gain access the database.

The database is also encrypted so if the database did get breached it would add another layer protection between us and the attackers.

The framework flask that we are using for our API endpoints requires users to have either a verified token or session to be able to 
upload any data at all to the API endpoint and therefore to the database. Any user passwords are also hashed and salted before storing them in 
the database also.

I believe that with the above approach to security it would make it extremely hard for the database to be breached and if someone were to try 
and get in they would be slowed to the point of extreme frustration and by that point an admin will hopefully know someone is trying 
to access the data.

Each country has their own privacy laws so it would be hard to write about them all so we will just go with Australia's, we have implemented 
data cleaning day to clean any data points that are over 28 days old as specified by the Australian data and privacy laws, a cronjob will run 
and erase any sign in records older than 28 days and destroy them.
 
#### The two authentication endpoints for this app will be:

* Flask-Login: This is a session based authentication service that will grant users permission on the front end using tokens 
and sessions.

* JWT: For the backend API to make it easy and also secure the app will issue tokens so integration with native mobile development 
can be seamless with the authentication process.

* CSRF Tokens: Issued to keep forms safe and to prevent cross site scripting attacks on users and the website.

#### User profiles:

There are four user profiles within the app:

* Anonymous user: Anyone that can use the sign in form to sign in to a venue or business.

* Registered user: A user that holds a profile with the app and stores data in the forms of posts and comments

* Registered business: This is an extension of the user profile where they have had their business application approved 
by an admin and can take sign ins for their venue or business.

* Admin user: A regular user account that has been granted admin permissions via a profile flag in the database. This 
user can approve new business applications and dump backups of the database to JSON via the admin panel.

## Discuss how you will address the following obligations as a developer:
- professional obligations (delivering the project on time, being explicit about ongoing maintenance of the system)

Delivery of code will be handled by the dev team through CI/CD piplines, the following branches ensure code does 
not get pushed into production unless it has been reviewed and tested:

* Feature branch - All new features will start off in a feature branch off from the dev branch, the person or team will push 
to their individual feature branch and once code has had tests implemented and they are passing it will be merged to the 
Dev branch

* Dev branch - Is the latest working development prototype of the project the branch will have a minimum of 90% code coverage 
to ensure that anything pushed to here is fully working like production before it is reviewed and merged with main branch.

* Main branch - The production branch that get's built and deployed to production, once tests are passed on dev, code reviewed 
and merged to this branch. GitHub actions then builds and deploys to the production server tearing down the old version and 
launching the new version.

Management and maintenance of the database will be handled with Flask addons such as:

* Flask-Migrate - This ensure that any changes to any any models are reflected and pushed to the production server while also 
storing a backup of previous migrations for easy roll back.

* PG_loader - This tool can be used to migrate all the data from one database to another, if we are doing backups or if we are 
moving from local to the cloud this tool will move everything safe and securely over SSH.

Project management is managed through GitHub boards so any any person or teams working on the project have immediate access 
to the [kanban](images/trello) style board.


- ethical obligations: ensuring that the application conforms with ethical codes of conduct approved by industry.

Ethically speaking we will not store any records of children under 13 in accordance to the law and just as stated above we also 
comply to the Australian data and privacy laws. We also do not accept sign ups from people of this ages as well.

We will go public with any data breaches and notify all parties who we hold data on.

We will not share any data with the venue of sign in unless the users have also opted in to doing so to join their mailing list or 
follow their accounts.



- legal obligations: that you have assessed whether the application is subject to any legal regulation, if none, consider any privacy implications.

Our legal obligation while storing data in Australia is to delete it ever 28 days and not store data on children under 13 which we 
do comply with. If by chance we have a covid outbreak in a venue with where our data is used, data will be handed over to contact tracers 
immediately.