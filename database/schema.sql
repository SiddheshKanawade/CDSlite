-- CREATE DATABASE CDSlite;
-- SHOW DATABASES;
USE CDSlite;

create table User(
UserID varchar(15) PRIMARY KEY,
FirstName varchar(25) NOT NULL,
LastName varchar(25),
Email_ID varchar(30) UNIQUE NOT NULL,
MobileNo char(10) NOT NULL,
Password_ varchar(30) NOT NULL,
DOB DATE,
Gender ENUM('M','F'),
AddressLine varchar(35),
City varchar(15),
PinCode char(7),
CONSTRAINT chk_email check (Email_ID like '%_@__%.__%'),
CONSTRAINT chk_mobile CHECK (MobileNo not like '%[^0-9]%')
)ENGINE = Innodb;

create table Seller(
SellerID varchar(15) PRIMARY KEY,
UserID varchar(15),
SoldProducts int DEFAULT 0,
BankName varchar(25),
AccountNo char(18),
IFSC_Code char(11),
Foreign Key(UserID) References User(UserID) ON DELETE CASCADE  
);

create table Category(
categoryID varchar(15) primary key,
catName varchar(40) not null
);

create table SubCategory(
SubcategoryID varchar(15) primary key,
subcatName varchar(40) not null
); 
create table Products(
ProductID varchar(15) primary key,
SellerID varchar(15),
foreign key(SellerID) References Seller(SellerID) ON DELETE CASCADE  
);

create table FP_Products(
ProductID varchar(15) primary key,
ProductName varchar(30) NOT NULL,
Description_ longtext,
Availability ENUM('Yes','No') NOT NULL,
MRP int NOT NULL,
Quantity int,
CreationDate Date default(current_date()),
UpdationDate Date default(current_date()),
CategoryID varchar(15) NOT NULL,
foreign key(ProductID) References Products(ProductID) ON DELETE CASCADE,
foreign key(CategoryID) References Category(CategoryID) ON DELETE CASCADE  
);

create table VP_Products(
ProductID varchar(15) primary key,
ProductName varchar(30) NOT NULL,
Description_ longtext,
Availability ENUM('Yes','No') NOT NULL,
BasePrice int NOT NULL,
isBarter ENUM('Yes','No') NOT NULL,
CreationDate Date default(current_date()),
UpdationDate Date default(current_date()),
CategoryID varchar(15) NOT NULL,
foreign key(ProductID) References Products(ProductID) ON DELETE CASCADE  ,
foreign key(CategoryID) References Category(CategoryID) ON DELETE CASCADE  
)ENGINE=InnoDB;

create table Unlisted_Products(
ProductID varchar(15) primary key,
ProductName varchar(30) NOT NULL,
Description_ longtext,
CreationDate date default(current_date()),
foreign key(ProductID) References Products(ProductID) ON DELETE CASCADE  
);

create table Order_(
OrderID varchar(15) primary key,
TotalPrice int,
DateCreated datetime default CURRENT_TIMESTAMP,
TransactionID varchar(20) unique NOT NULL
);

create table BidTable(
BidID varchar(15) primary key,
ProductID varchar(15),
UserID varchar(15),
BidDate datetime default CURRENT_TIMESTAMP,
BidPrice int NOT NULL,
BidStatus ENUM('Confirmed','Pending','Declined'),
Foreign key (ProductID) References Products(ProductID) ON DELETE CASCADE,
Foreign key (UserID) References User(UserID) ON DELETE CASCADE 
);

create table ShoppingCart(
UserID varchar(15),
ProductID varchar(15),
Quantity int,
DateAdded datetime default CURRENT_TIMESTAMP,
foreign key(UserID) references User(UserID) ON DELETE CASCADE,
foreign key(ProductID) references Products(ProductID) ON DELETE CASCADE,
primary key(UserID, ProductID)
);

create table Variant(
VariantID varchar(15),
ProductID varchar(15) not null,
foreign key(ProductID) references Products(ProductID) ON DELETE CASCADE,
primary key (VariantID, ProductID)
);

create table Barter(
BarterID varchar(15) NOT NULL,
P1ID varchar(15) NOT NULL, 
P2ID varchar(15) NOT NULL,
BarterStatus enum("Accepted", "Declined", "Pending") NOT NULL,
BarterDate Datetime default CURRENT_TIMESTAMP,
foreign key(P1ID) references Products(ProductID) ON DELETE CASCADE,
foreign key(P2ID) references Products(ProductID) ON DELETE CASCADE,
primary key(BarterID)
);

create table isMerchant (
SellerID varchar(15) primary key,
OrgName varchar(20) unique NOT NULL,
foreign key(SellerID) references Seller(SellerID) ON DELETE CASCADE
);


create table Payments(
OrderID varchar(15),
UserID varchar(15),
ProductID varchar(15),
Status_ ENUM('Successful', 'Failed'),
foreign key(OrderID) references Order_(OrderID) ON DELETE CASCADE,
foreign key(ProductID) references Products(ProductID) ON DELETE CASCADE,
foreign key(UserID) references User(UserID) ON DELETE CASCADE,
primary key(OrderID, ProductID)
);

create table Constrained (
CategoryID varchar(15),
SubCategoryID varchar(15),
foreign key(CategoryID) references Category(CategoryID) ON DELETE CASCADE,
foreign key(SubCategoryID) references SubCategory(SubCategoryID) ON DELETE CASCADE,
primary key(CategoryID, SubCategoryID)
);

create table FPhasSubCat (
ProductID varchar(15),
SubCategoryID varchar(15),
foreign key(ProductID) references Products(ProductID) ON DELETE CASCADE,
foreign key(SubCategoryID) references SubCategory(SubCategoryID) ON DELETE CASCADE,
primary key(ProductID, SubCategoryID)
);

create table VPhasSubCat (
ProductID varchar(15),
SubCategoryID varchar(15),
foreign key(ProductID) references Products(ProductID) ON DELETE CASCADE,
foreign key(SubCategoryID) references SubCategory(SubCategoryID) ON DELETE CASCADE,
primary key(ProductID, SubCategoryID)
);

create table BarterHistory(
BarterID varchar(15),
OrderID varchar(15),
OrderDate datetime default CURRENT_TIMESTAMP,
foreign key(BarterID) references Barter(BarterID) ON DELETE CASCADE,
foreign key(OrderID) references Order_(OrderID) ON DELETE CASCADE,
primary key(OrderID)
);

COMMIT;
