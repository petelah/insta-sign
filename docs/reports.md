### Discuss how the application will handle the privacy of user data within the system, and how security features of the frameworks you are utilising will assist to mitigate security concerns.


SQL Alchemy mitigates the risk of dealing with the threat of SQL injection attack by sanitising data input and output to and from the user. 
It essentially sits there as a gatekeeper or firewall for the data.

By sanitising and validating the data before it gets to the database the risk of a threat actor sending an injection attack is very low.

We also place the database behind a private subnet so the api gateway machine is the only input and output to the database. 
This allows up to control the flow of data through the ORM with sanitisation and validation as stated above and it also makes 
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
 and gran any sign in records older than 28 days and destroy them.

### Discuss how you will address the following obligations as a developer:
- professional obligations (delivering the project on time, being explicit about ongoing maintenance of the system)

I will keep myself at task by treating my project days like work days, 9-5 I will be working on the project with a lunch break and 
will implement the use of project management and tracking tools such as trello and github.


- ethical obligations: ensuring that the application conforms with ethical codes of conduct approved by industry.

Ethically speaking we will not store any records of children under 13 in accordance to the law and just as stated above we also 
comply to the Australian data and privacy laws. 

We will go public with any data breaches and notify all parties who we hold data on.

We will not share any data with the venue of sign in unless the users have also opted in to doing so to join their mailing list or 
follow their accounts.



- legal obligations: that you have assessed whether the application is subject to any legal regulation, if none, consider any privacy implications.

Our legal obligation while storing data in Australia is to delete it ever 28 days and not store data on children under 13 which we 
do comply with. If by chance we have a covid outbreak in a venue with where our data is used, data will be handed over to contact tracers 
immediately.