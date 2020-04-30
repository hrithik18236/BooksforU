CREATE TABLE `review` (
   `user_id` INT NOT NULL,
   `title` varchar(255) NOT NULL,
   `body` varchar(255) NOT NULL,
   `unique_id` INT NOT NULL,
   PRIMARY KEY (`user_id`,`unique_id`),
   INDEX (`user_id`,`unique_id`)
);
 
CREATE TABLE `archive` (
   `archive_id` INT NOT NULL,
   `unique_id` INT NOT NULL,
   `user_id` INT NOT NULL,
   `transaction_type` INT NOT NULL,
   PRIMARY KEY (`archive_id`),
   INDEX (`archive_id`)
);

CREATE INDEX idx_archive_book ON archive(archive_id,unique_id);
 
CREATE TABLE `all_books` (
   `book_id` INT NOT NULL,
   `description` varchar(1024) NOT NULL,
   `page_count` INT NOT NULL,
   `transaction_type` INT NOT NULL,
   `unique_id` INT NOT NULL,
   `user_id` INT NOT NULL,
   PRIMARY KEY (`book_id`),
   INDEX (`book_id`)
);
 
CREATE INDEX idx_all_books_unique ON all_books(unique_id);
 
CREATE TABLE `genre` (
   `genre_name` varchar(30) NOT NULL,
   PRIMARY KEY (`genre_name`),
   INDEX (`genre_name`)
);
 
CREATE TABLE `available_for_borrowing` (
   `book_id` INT NOT NULL,
   `price` INT NOT NULL,
   `num_of_days` INT NOT NULL,
   PRIMARY KEY (`book_id`),
   INDEX (`book_id`)
);
 
CREATE INDEX idx_avail_borrow_price ON available_for_borrowing(price);
CREATE INDEX idx_avail_borrow_days ON available_for_borrowing(num_of_days);
 
CREATE TABLE `unique_books` (
   `unique_id` INT NOT NULL AUTO_INCREMENT,
   `name` varchar(255) NOT NULL,
   `author` varchar(255) NOT NULL,
   `rating` FLOAT NOT NULL,
   `review_count` INT NOT NULL,
   `recommendation_count` INT NOT NULL,
   `book_count` INT NOT NULL,
   PRIMARY KEY (`unique_id`),
   INDEX (`unique_id`)
);
 
CREATE INDEX idx_unique_books_count ON unique_books(book_count);
CREATE INDEX idx_unique_books_name ON unique_books(name);
CREATE INDEX idx_unique_books_author ON unique_books(author);
CREATE INDEX idx_unique_books_rating ON unique_books(rating);
CREATE INDEX idx_unique_books_recom ON unique_books(recommendation_count);
 
CREATE TABLE `user` (
   `user_id` INT NOT NULL,
   `name` varchar(255) NOT NULL,
   `user_type` INT NOT NULL,
   `email_id` varchar(255) NOT NULL,
   `contact_num` varchar(10) NOT NULL,
   `location` varchar(10) NOT NULL,
   `password` varchar(10) NOT NULL,
   PRIMARY KEY (`user_id`),
   INDEX (`user_id`)
);

CREATE INDEX idx_user_name ON user(name);
CREATE INDEX idx_user_location ON user(location);
 
CREATE TABLE `available_for_buying` (
   `book_id` INT NOT NULL,
   `price` INT NOT NULL,
   PRIMARY KEY (`book_id`),
   INDEX (`book_id`)
);

CREATE INDEX idx_avail_buy_price ON available_for_buying(price);
 
CREATE TABLE `available_for_exchange` (
   `book_id` INT NOT NULL,
   `exchange_with` varchar(255) NOT NULL,
   PRIMARY KEY (`book_id`),
   INDEX (`book_id`)
);
 
CREATE TABLE `book_genre_relation` (
   `unique_id` INT NOT NULL,
   `genre_name` varchar(30) NOT NULL,
   PRIMARY KEY (`unique_id`,`genre_name`),
   INDEX (`unique_id`,`genre_name`)
);
 
CREATE TABLE `preferences` (
   `user_id` INT NOT NULL,
   `genre_name` varchar(30) NOT NULL,
   `user_type` INT NOT NULL,
   PRIMARY KEY (`user_id`,`genre_name`),
   INDEX (`user_id`,`genre_name`)
);
 
CREATE TABLE `recommendations` (
   `user_id` INT NOT NULL,
   `unique_id` INT NOT NULL,
   PRIMARY KEY (`unique_id`,`user_id`),
   INDEX (`unique_id`,`user_id`)
);

CREATE INDEX idx_book_genre_rel_genre_name ON book_genre_relation(genre_name);
 
ALTER TABLE `review` ADD CONSTRAINT `review_fk0` FOREIGN KEY (`unique_id`) REFERENCES `unique_books`(`unique_id`);
 
ALTER TABLE `review` ADD CONSTRAINT `review_fk1` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);
 
ALTER TABLE `archive` ADD CONSTRAINT `archive_fk0` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);
 
ALTER TABLE `all_books` ADD CONSTRAINT `all_books_fk0` FOREIGN KEY (`unique_id`) REFERENCES `unique_books`(`unique_id`);
 
ALTER TABLE `available_for_borrowing` ADD CONSTRAINT `available_for_borrowing_fk0` FOREIGN KEY (`book_id`) REFERENCES `all_books`(`book_id`);
 
ALTER TABLE `available_for_buying` ADD CONSTRAINT `available_for_buying_fk0` FOREIGN KEY (`book_id`) REFERENCES `all_books`(`book_id`);
 
ALTER TABLE `available_for_exchange` ADD CONSTRAINT `available_for_exchange_fk0` FOREIGN KEY (`book_id`) REFERENCES `all_books`(`book_id`);
 
ALTER TABLE `book_genre_relation` ADD CONSTRAINT `book_genre_relation_fk0` FOREIGN KEY (`unique_id`) REFERENCES `unique_books`(`unique_id`);
 
ALTER TABLE `book_genre_relation` ADD CONSTRAINT `book_genre_relation_fk1` FOREIGN KEY (`genre_name`) REFERENCES `genre`(`genre_name`);
 
ALTER TABLE `preferences` ADD CONSTRAINT `perferences_fk0` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);
 
ALTER TABLE `preferences` ADD CONSTRAINT `perferences_fk1` FOREIGN KEY (`genre_name`) REFERENCES `genre`(`genre_name`);
 
ALTER TABLE `recommendations` ADD CONSTRAINT `recommendations_fk0` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`);
 
ALTER TABLE `recommendations` ADD CONSTRAINT `recommendations_fk1` FOREIGN KEY (`unique_id`) REFERENCES `unique_books`(`unique_id`);
 
alter table unique_books
add constraint CHK_RATING CHECK (rating >= 0 and rating <= 10);
 
alter table all_books
add constraint TRANS_CHECK CHECK (transaction_type >= 1 and transaction_type <= 3);
 
alter table archive
add constraint TRANS_CHECK2 CHECK (transaction_type >= 1 and transaction_type <= 3);
 
alter table available_for_borrowing
add constraint PRICE_CHECK CHECK (price >= 0);
 
alter table available_for_buying
add constraint PRICE_CHECK2 CHECK (price >= 0);
 
insert into user (user_id, name, email_id, contact_num, coins) values (1, 'Leighton Sandys', 'lsandys0@domainmarket.com', '8466266364', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (2, 'Amberly Rainbird', 'arainbird1@163.com', '9997329196', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (3, 'Pauline Eskriet', 'peskriet2@about.me', '9347776135', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (4, 'Xever Shimwall', 'xshimwall3@so-net.ne.jp', '4986566256', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (5, 'Joseph Badwick', 'jbadwick4@mapquest.com', '1008200222', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (6, 'Tadeas Wortman', 'twortman5@oaic.gov.au', '3106924923', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (7, 'Irvine Wetherell', 'iwetherell6@infoseek.co.jp', '2841948157', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (8, 'Sarita Cuschieri', 'scuschieri7@salon.com', '2585811497', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (9, 'Tatum McGillivrie', 'tmcgillivrie8@hhs.gov', '5299551156', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (10, 'Yolande Leitch', 'yleitch9@angelfire.com', '1687830487', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (11, 'Curr Guerreiro', 'cguerreiroa@mediafire.com', '3944218416', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (12, 'Elysha Mallalieu', 'emallalieub@oakley.com', '4672804938', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (13, 'Bartram Pauletto', 'bpaulettoc@soup.io', '1062310823', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (14, 'Carce McDiarmid', 'cmcdiarmidd@163.com', '5886230109', 0);
insert into user (user_id, name, email_id, contact_num, coins) values (15, 'Niki Arnli', 'narnlie@si.edu', '7299888297', 0);

insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (1, 'Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus. Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis.', 876, 1, 1);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (2, 'Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi.', 372, 1, 10);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (3, 'Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.', 376, 3, 10);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (4, 'Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus.', 133, 2, 4);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (5, 'Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus.', 231, 3, 4);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (6, 'Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus. In sagittis dui vel nisl. Duis ac nibh.', 998, 2, 3);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (7, 'Nulla tellus. In sagittis dui vel nisl. Duis ac nibh.', 813, 2, 3);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (8, 'Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo.', 961, 2, 3);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (9, 'Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam. Suspendisse potenti.', 853, 3, 2);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (10, 'Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst.', 837, 1, 6);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (11, 'Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit.', 86, 3, 6);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (12, 'Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 274, 3, 6);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (13, 'In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis.', 388, 1, 8);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (14, 'Aliquam erat volutpat.', 843, 2, 8);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (15, 'In congue.', 86, 1, 5);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (16, 'In sagittis dui vel nisl. Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti. In eleifend quam a odio. In hac habitasse platea dictumst. Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat.', 180, 2, 5);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (17, 'Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus.', 622, 2, 9);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (18, 'In congue. Etiam justo.', 116, 1, 7);
insert into all_books (book_id, description, page_count, transaction_type, unique_id) values (19, 'Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi.', 570, 2, 7);
 
insert into recommendations (user_id, unique_id) values (1, 9);
insert into recommendations (user_id, unique_id) values (2, 2);
insert into recommendations (user_id, unique_id) values (3, 13);
insert into recommendations (user_id, unique_id) values (4, 1);
insert into recommendations (user_id, unique_id) values (5, 8);

insert into available_for_borrowing (book_id, price, num_of_days) values (1, 375, 85);
insert into available_for_borrowing (book_id, price, num_of_days) values (2, 503, 204);
insert into available_for_borrowing (book_id, price, num_of_days) values (10, 674, 316);
insert into available_for_borrowing (book_id, price, num_of_days) values (13, 557, 184);
insert into available_for_borrowing (book_id, price, num_of_days) values (15, 804, 188);
insert into available_for_borrowing (book_id, price, num_of_days) values (18, 500, 313);
 
insert into available_for_buying (book_id, price) values (3, 631);
insert into available_for_buying (book_id, price) values (5, 392);
insert into available_for_buying (book_id, price) values (9, 293);
insert into available_for_buying (book_id, price) values (11, 667);
insert into available_for_buying (book_id, price) values (12, 483);
 
insert into available_for_exchange (book_id, exchange_with) values (4, 'Children of Men');
insert into available_for_exchange (book_id, exchange_with) values (6, 'Playing It Cool');
insert into available_for_exchange (book_id, exchange_with) values (7, 'Better Luck Tomorrow');
insert into available_for_exchange (book_id, exchange_with) values (8, 'My Girl');
insert into available_for_exchange (book_id, exchange_with) values (14, 'Return to House on Haunted Hill');
insert into available_for_exchange (book_id, exchange_with) values (16, 'Alila');
insert into available_for_exchange (book_id, exchange_with) values (17, 'Ecstasy (Éxtasis)');
insert into available_for_exchange (book_id, exchange_with) values (19, 'Robber, The (Der Räuber)');
 
insert into book_genre_relation (unique_id, genre_name) values (1, 'Horror');
insert into book_genre_relation (unique_id, genre_name) values (1, 'Mystery');
insert into book_genre_relation (unique_id, genre_name) values (2, 'Horror');
insert into book_genre_relation (unique_id, genre_name) values (3, 'Physics');
insert into book_genre_relation (unique_id, genre_name) values (3, 'Non-fiction');
insert into book_genre_relation (unique_id, genre_name) values (4, 'Thriller');
insert into book_genre_relation (unique_id, genre_name) values (5, 'Romance');
insert into book_genre_relation (unique_id, genre_name) values (5, 'Action');
insert into book_genre_relation (unique_id, genre_name) values (6, 'Horror');
insert into book_genre_relation (unique_id, genre_name) values (6, 'Mystery');
insert into book_genre_relation (unique_id, genre_name) values (6, 'Thriller');
insert into book_genre_relation (unique_id, genre_name) values (7, 'Horror');
insert into book_genre_relation (unique_id, genre_name) values (7, 'Thriller');
insert into book_genre_relation (unique_id, genre_name) values (8, 'Action');
insert into book_genre_relation (unique_id, genre_name) values (9, 'Comic');
insert into book_genre_relation (unique_id, genre_name) values (9, 'Action');
insert into book_genre_relation (unique_id, genre_name) values (10, 'Horror');
insert into book_genre_relation (unique_id, genre_name) values (10, 'Mystery');
 
insert into genre (genre_name, book_count) values ('Horror', 2);
insert into genre (genre_name, book_count) values ('Thriller', 2);
insert into genre (genre_name, book_count) values ('Romance', 2);
insert into genre (genre_name, book_count) values ('Mystery', 2);
insert into genre (genre_name, book_count) values ('Action', 2);
insert into genre (genre_name, book_count) values ('Non-fiction', 2);
insert into genre (genre_name, book_count) values ('Physics', 2);
insert into genre (genre_name, book_count) values ('Comic', 2);
 
insert into review (user_id, title, body, unique_id) values (1, 'sed magna at', 'Melita Heintzsch', 'Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.', 1);
insert into review (user_id, title, body, unique_id) values (2, 'ut erat curabitur', 'Latrena Byrth', 'Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim.', 1); insert into review (user_id, title, author, body, unique_id) values (3, 'vel enim sit amet', 'Harley Siddon', 'Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum.', 1);
insert into review (user_id, title, body, unique_id) values (4, 'volutpat erat quisque erat', 'Viviyan Erricker', 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem.', 1);
insert into review (user_id, title, body, unique_id) values (5, 'leo odio condimentum', 'Olly Bellay', 'Etiam justo. Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna.', 2);
insert into review (user_id, title, body, unique_id) values (6, 'ridiculus mus vivamus vestibulum', 'Shermy Menary', 'Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat.', 2);
insert into review (user_id, title, body, unique_id) values (7, 'dui maecenas tristique est et', 'Levi Bimrose', 'Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat.', 2);
insert into review (user_id, title, body, unique_id) values (8, 'odio elementum eu', 'Ronald Bernini', 'Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est.', 2);
insert into review (user_id, title, body, unique_id) values (9, 'iaculis congue vivamus metus arcu', 'Donni Kleinstein', 'Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla. Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam.', 3);
insert into review (user_id, title, body, unique_id) values (10, 'habitasse platea dictumst', 'Rodger Cottingham', 'Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus.', 3);
insert into review (user_id, title, body, unique_id) values (11, 'in hac habitasse platea dictumst', 'Flss Beatens', 'Praesent blandit. Nam nulla.', 4);
insert into review (user_id, title, body, unique_id) values (12, 'diam vitae quam suspendisse potenti', 'Myles Iliffe', 'Donec posuere metus vitae ipsum. Aliquam non mauris.', 4);
insert into review (user_id, title, body, unique_id) values (13, 'nibh in quis justo maecenas', 'Jakie Pallister', 'Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est.', 4);
insert into review (user_id, title, body, unique_id) values (14, 'orci eget orci vehicula', 'Gal Balshaw', 'Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue.', 4);
insert into review (user_id, title, body, unique_id) values (15, 'odio odio elementum eu', 'Retha Rumney', 'Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus. Pellentesque eget nunc.', 4);
insert into review (user_id, title, body, unique_id) values (16, 'sed vel enim', 'Marys Lantaff', 'Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.', 4);
insert into review (user_id, title, body, unique_id) values (17, 'fermentum donec ut', 'Perri Darch', 'Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor. Duis mattis egestas metus.', 4);
insert into review (user_id, title, body, unique_id) values (18, 'adipiscing molestie hendrerit at', 'Hedvig Brockhurst', 'Donec posuere metus vitae ipsum. Aliquam non mauris.', 4);
insert into review (user_id, title, body, unique_id) values (19, 'phasellus sit amet erat nulla', 'Agosto Alfonsetti', 'Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat.', 4);
insert into review (user_id, title, body, unique_id) values (20, 'nam tristique tortor eu', 'Melania Tudbald', 'Aenean fermentum. Donec ut mauris eget massa tempor convallis.', 4);
insert into review (user_id, title, body, unique_id) values (21, 'eu massa donec dapibus', 'Diahann Huddy', 'Aliquam erat volutpat. In congue. Etiam justo. Etiam pretium iaculis justo.', 5);
insert into review (user_id, title, body, unique_id) values (22, 'augue quam sollicitudin vitae', 'Sile Neissen', 'Pellentesque ultrices mattis odio. Donec vitae nisi.', 5);
insert into review (user_id, title, body, unique_id) values (23, 'nunc purus phasellus in', 'Lenard Heaps', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum.', 5);
insert into review (user_id, title, body, unique_id) values (24, 'pharetra magna ac consequat', 'Lois Spurdens', 'Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.', 5);
insert into review (user_id, title, body, unique_id) values (25, 'ultrices libero non mattis pulvinar', 'Elmer Itzkovwich', 'Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 8);
insert into review (user_id, title, body, unique_id) values (26, 'interdum venenatis turpis', 'Lotti Wratten', 'Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum.', 8);
insert into review (user_id, title, body, unique_id) values (27, 'est donec odio justo sollicitudin', 'Beitris O''Henecan', 'Vivamus tortor. Duis mattis egestas metus. Aenean fermentum.', 8);
insert into review (user_id, title, body, unique_id) values (28, 'pharetra magna ac consequat', 'Rey Keegan', 'Etiam justo. Etiam pretium iaculis justo.', 9);
insert into review (user_id, title, body, unique_id) values (29, 'odio porttitor id consequat in', 'Quint Rigeby', 'Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero.', 9);
insert into review (user_id, title, body, unique_id) values (30, 'ante ipsum primis', 'Junina Paulmann', 'Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.', 9);
insert into review (user_id, title, body, unique_id) values (31, 'vel nisl duis ac', 'Faythe Cullip', 'Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim.', 10);
insert into review (user_id, title, body, unique_id) values (32, 'tempus vel pede morbi porttitor', 'Agneta Swait', 'Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus. In sagittis dui vel nisl. Duis ac nibh.', 10);
insert into review (user_id, title, body, unique_id) values (33, 'vel est donec', 'Kaja Legges', 'Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus.', 10);
 
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (1, 'Warlock', 'Noelani Petel', 3.4, 4, 5, 1);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (2, 'April''s Shower', 'Elise Burch', 1.6, 4, 4, 1);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (3, 'Woman in Red, The', 'Alameda Milvarnie', 3.1, 2, 1, 3);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (4, 'Elia Kazan: A Director''s Journey', 'Hilliard Linscott', 2.5, 10, 3, 2);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (5, 'Give My Regards to Broad Street', 'Warden Von Welldun', 4.2, 4, 1, 2);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (6, 'Barber, The', 'Silvie Kluger', 5.2, 0, 3, 3);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (7, 'The Moromete Family', 'Kary Dockrill', 1.5, 0, 0, 2);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (8, 'Aziz Ansari: Dangerously Delicious', 'Anne Litherland', 7.9, 3, 2, 2);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (9, 'No Way Out', 'Dani Peartree', 9.4, 3, 1, 1);
insert into unique_books (unique_id, name, author, rating, review_count, recommendation_count, book_count) values (10, 'Adventures of the Wilderness Family, The', 'Roderick Boman', 8.5, 3, 5, 2);

insert into archive (archive_id, unique_id, user_id, transaction_type) values (1, 20, 3, 1);
insert into archive (archive_id, unique_id, user_id, transaction_type) values (2, 21, 4, 2);