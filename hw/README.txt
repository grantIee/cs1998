Name: Grant Lee
NetID: ghl35
Issues:
- I am trying to make my code more shorter and easier to read:
	- I've noticed that I have put this parameter to check if the fields from the body is a blankstring. I'm not exactly sure how to handle most of these cases where the body or header can either be blank or be entirely null in the most concise way. 

	- Will the database ever need to make the vote an object? When users are added to this database and we want to keep a running track of what each user votes on, how would we keep track of such a thing? I know that this is a bit ahead, but I've been thinking about how FB or Reddit actually keeps tracks of these logistics. That's a lot of data, and I was wondering if that was the best way of doing it?

Extensions: None
Comments:
I was confused whether the input from the header for the voting functions should all be the post_id, but I thought about it and considered that the vote should apply to the comment itself when voting on comments. I thought that this would be the best integration because each comment object has its own id field. 
