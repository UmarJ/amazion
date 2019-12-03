/*Create schema onlineStore;*/
create table Account(
AccountID varchar(10),
Email varchar(50),
FirstName char(10),
LastName char(10),
gender ENUM('male', 'female') NOT NULL,
dateCreated timestamp,
passwordHash varchar(10),
salt varchar(4),
phone integer(11),
AccountBalance decimal,
PRIMARY KEY (AccountID)
);

create table Ordear(
orderID varchar(10),
ampunt decimal,
Date timestamp,
OrderCompleted boolean,
cartID varchar(10),

primary key (orderID)
);

Create table TransactionHistory(
AccountID varchar(10),
changeAmount decimal,
TransactionDate timestamp,
TransactionID varchar(10),
OrderID varchar(10),
PRIMARY KEY (TransactionID),
FOREIGN KEY (AccountID) REFERENCES Account(AccountID),
FOREIGN KEY (OrderID) REFERENCES Ordear(orderID));


create table Customer(
customerID varchar(10),
AccountID varchar(10),
primary key (AccountID),
unique (customerID),
FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
);

create table Seller(
AccountID varchar(10),
SellerID varchar(10),
Rating int(1),

primary key (AccountID),
unique (sellerID),
foreign key (AccountID) references Account(AccountID)
);

create table Cart(
CustomerID varchar(10),
dateAdded timestamp,
CartID varchar(10),

primary key (CartID),
foreign key (CustomerID) references Customer(customerID));


create table Deal(
dealID varchar(10),
percentage integer(2),
Description char(250),

primary key(dealID)
);

create table Category(
categoryID varchar(10),
ParentCategoryID varchar(10),
CategoryName char(20),
Description char(250),

primary key (categoryID));

create table Product(
productID varchar(10),
dealID varchar(10),
narrowestCategoryID varchar(10),
Name char(10),
description char(250),
price decimal,
imagepath varchar(100),
Isavailable bool,
CartID varchar(10),
CategoryID varchar(10),
SellerID varchar(10),

primary key (productID),
foreign key (dealID) references deal(dealID),
foreign key (narrowestCategoryID) references Category(categoryID),
foreign key (cartID) references cart (cartID),
foreign key (sellerID) references seller (sellerID)
);



create table DealHistory(
dealID varchar(10),
dealStart timestamp,
dealEnd timestamp,

primary key(dealID,dealStart,dealEnd),
foreign key (dealID) references deal (dealID)
);



create table Review(
productID varchar(10),
reviewID varchar(10),
reviewStars int(1),
reviewText char(250),
reviewerID varchar(10),
WasBought boolean,
Images varchar(10),
primary key (reviewID),
foreign key (productID) references product (productID));


create table ReviewImage(
reviewID varchar(10),
Image varchar(10),

primary key (reviewID,Image),
foreign key (reviewID) references Review (reviewID));

create table ReviewRating(
reviewID varchar(10),
ratedBy char(10),
helpful boolean,

primary key (reviewID,ratedBy),
foreign key (reviewID) references Review (reviewID)
);

create table Address(
addressID varchar(10),
House varchar(10),
Street varchar(10),
City char(20),
Country char(20),
CustomerID varchar(10),

primary key (addressID,CustomerID),
foreign key (CustomerID) references Customer (customerID)
);

create table Question(
productID varchar(10),
questionID varchar(10),
askedBy char(10),
texty char(250),
unique (questionID),
primary key (productID,questionID),
foreign key (productID) references product(productID)
);
create table Answer(
answerID varchar(10),
questionID varchar(10),
ansBy char(20),
texty char(250),
unique (answerID),
primary key (answerID,questionID),
foreign key (questionID) references Question(questionID)
);

create table AnswerRating(
answerID varchar(10),
ratedBy char(10),
helpful boolean,

primary key (answerID,ratedBy),
foreign key (answerID) references answer (answerID)
);
