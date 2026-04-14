CREATE DATABASE PI;
USE PI;
CREATE TABLE candidatos(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
numero INT UNIQUE,
partido VARCHAR(100)
);

Insert Into candidatos (nome, numero, partido)
VALUES ('Marina',  15, 'PTBS'), 
	   ('Matheus', 17, 'ASDT'),
       ('Rafae', 12, 'JTPO');


CREATE TABLE eleitor(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
cpf INT(11) UNIQUE NOT NULL,
numemro_titulo INT UNIQUE NOT NULL,
chave_de_acesso INT(4),
mesario BOOLEAN DEFAULT FALSE,
status_de_voto BOOLEAN DEFAULT FALSE
);


CREATE TABLE votos(
id INT AUTO_INCREMENT PRIMARY KEY,
protocolo_voto VARCHAR(100) UNIQUE,
voto int,
data_hora DATETIME
);