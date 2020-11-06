CREATE database test;

use test;

CREATE TABLE dozenDuty_app_member(
	memberID 	INT unsigned AUTO_INCREMENT, 
	memberName	VARCHAR(20),
	PRIMARY KEY (memberID)
);

CREATE TABLE dozenDuty_app_home(
	homeID 	INT unsigned AUTO_INCREMENT, 
	memberID 	INT unsigned,
	homeName	VARCHAR(20) NOT NULL ,
	PRIMARY KEY(homeID, memberID),
	FOREIGN KEY (memberID) REFERENCES dozenDuty_app_member(memberID)
);

CREATE TABLE dozenDuty_app_grocery(
	groceryID 	INT unsigned AUTO_INCREMENT, 
    groceryName VARCHAR(40),
	memberID	INT unsigned, 
	unitPrice	REAL unsigned, 
	quantity	INT unsigned DEFAULT 0, 
	purchaseDate	DATE NOT NULL, 
	ExpirationDate	DATE, 
	ItemType	VARCHAR(20),
	PRIMARY KEY (groceryID),
	FOREIGN KEY (memberID) REFERENCES dozenDuty_app_member(memberID)
);

CREATE TABLE dozenDuty_app_chore(
	choreID	INT unsigned AUTO_INCREMENT, 
	memberID	INT unsigned, 
	name		VARCHAR(20), 
	dueDate	DATE NOT NULL, 
	status		VARCHAR(5), 
	steps		INT NOT NULL DEFAULT 1,
	PRIMARY KEY  (choreID),
	FOREIGN KEY  (memberID) REFERENCES dozenDuty_app_member(memberID)
);

CREATE TABLE dozenDuty_app_contain(
	memberID 	INT unsigned AUTO_INCREMENT,
	homeID 	INT unsigned, 
	PRIMARY KEY (memberID,homeID),
	FOREIGN KEY (memberID) REFERENCES dozenDuty_app_member(memberID),
	FOREIGN KEY (homeID) REFERENCES dozenDuty_app_home(homeID)
);

CREATE TABLE dozenDuty_app_shop(
	groceryID	INT unsigned AUTO_INCREMENT,
	homeID	INT unsigned,
	PRIMARY KEY(groceryID, homeID),
	FOREIGN KEY (groceryID) REFERENCES dozenDuty_app_grocery(groceryID),
	FOREIGN KEY (homeID) REFERENCES dozenDuty_app_home(homeID)
);



CREATE TABLE dozenDuty_app_does(
	choreID	INT unsigned AUTO_INCREMENT,
	homeID	INT unsigned,
	PRIMARY KEY(choreID, homeID),
	FOREIGN KEY (choreID) REFERENCES dozenDuty_app_chore(choreID),
	FOREIGN KEY (homeID) REFERENCES dozenDuty_app_home(homeID)
);