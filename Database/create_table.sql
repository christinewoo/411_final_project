CREATE TABLE Member(
	memberID 	INT unsigned AUTO_INCREMENT, 
	memberName	VARCHAR(20),
	PRIMARY KEY (memberID)
);

CREATE TABLE Home(
	homeID 	INT unsigned AUTO_INCREMENT, 
	memberID 	INT unsigned,
	homeName	CHAR(20) NOT NULL ,
	PRIMARY KEY(homeID, memberID),
	FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE Grocery(
	groceryID 	INT unsigned AUTO_INCREMENT, 
	memberID	INT unsigned, 
	unitPrice	REAL unsigned, 
	quantity	INT unsigned DEFAULT 0, 
	purchaseDate	DATE NOT NULL, 
	ExpirationDate	DATE, 
	ItemType	VARCHAR(20),
	PRIMARY KEY (groceryID),
	FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE Chore(
	choreID	INT unsigned AUTO_INCREMENT, 
	memberID	INT unsigned, 
	name		VARCHAR(20), 
	dueDate	DATE NOT NULL, 
	status		VARCHAR(5), 
	steps		INT NOT NULL DEFAULT 1,
	PRIMARY KEY  (choreID),
	FOREIGN KEY  (memberID) REFERENCES Member(memberID)
);

CREATE TABLE Contain(
	memberID 	INT unsigned AUTO_INCREMENT,
	homeID 	INT unsigned, 
	PRIMARY KEY (memberID,homeID),
	FOREIGN KEY (memberID) REFERENCES Member(memberID),
	FOREIGN KEY (homeID) REFERENCES Home(homeID)
);

CREATE TABLE Shop(
	groceryID	INT unsigned AUTO_INCREMENT,
	homeID	INT unsigned,
	PRIMARY KEY(groceryID, homeID),
	FOREIGN KEY (groceryID) REFERENCES Grocery(groceryID),
	FOREIGN KEY (homeID) REFERENCES Home(homeID),
);



CREATE TABLE Does(
	choreID	INT unsigned AUTO_INCREMENT,
	homeID	INT unsigned,
	PRIMARY KEY(choreID, homeID),
	FOREIGN KEY (choreID) REFERENCES Chore(choreID),
	FOREIGN KEY (homeID) REFERENCES Home(homeID),
);