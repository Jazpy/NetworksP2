DROP USER 'pokeuser'@'localhost';
DROP DATABASE pokedex;

CREATE USER 'pokeuser'@'localhost' IDENTIFIED BY 'poke';

CREATE DATABASE pokedex;

GRANT ALL PRIVILEGES ON pokedex.* TO 'pokeuser'@'localhost';

FLUSH PRIVILEGES;

use pokedex;

CREATE TABLE pokemon
(
	pokemon_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255),
	image_path VARCHAR(255)
);

CREATE TABLE users
(
	user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255)
);

CREATE TABLE caught
(
	user_id INT NOT NULL,
	pokemon_id INT NOT NULL
);

INSERT INTO pokemon (name, image_path) VALUES ('Pikachu', '../db/images/pikachu.png');
INSERT INTO pokemon (name, image_path) VALUES ('Bulbasaur', '../db/images/bulbasaur.png');
INSERT INTO pokemon (name, image_path) VALUES ('Charmander', '../db/images/charmander.png');
INSERT INTO pokemon (name, image_path) VALUES ('Squirtle', '../db/images/squirtle.png');
INSERT INTO pokemon (name, image_path) VALUES ('Charizard', '../db/images/charizard.png');
INSERT INTO pokemon (name, image_path) VALUES ('Venosaur', '../db/images/venosaur.png');
INSERT INTO pokemon (name, image_path) VALUES ('Blastoise', '../db/images/blastoise.png');
INSERT INTO pokemon (name, image_path) VALUES ('Scyther', '../db/images/scyther.png');
INSERT INTO pokemon (name, image_path) VALUES ('Articuno', '../db/images/articuno.png');
INSERT INTO pokemon (name, image_path) VALUES ('Goldeen', '../db/images/goldeen.png');

INSERT INTO users (name) VALUES ('Ash');
