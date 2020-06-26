

CREATE DATABASE shapeit;

USE shapeit;

CREATE TABLE user(
  id int NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,  
  username varchar(80) NOT NULL,
  email varchar(120) NOT NULL, 
  password varchar(180) NOT NULL, 
  profile varchar(80) DEFAULT 'default.jpg',
  PRIMARY KEY (id)

  );

CREATE TABLE addproduct(
  id int NOT NULL AUTO_INCREMENT, 
  name varchar(255) NOT NULL,  
  price varchar(255) NOT NULL, 
  discount varchar(255) NOT NULL, 
  stock varchar(255) NOT NULL, 
  colors varchar(255) NOT NULL, 
  desc varchar(255) NOT NULL, 
  pub_date DATETIME NOT NULL,
  category_id int(255) NOT NULL,
  
  PRIMARY KEY (id),
  FOREIGN KEY (category_id) REFERENCES category(id)
);