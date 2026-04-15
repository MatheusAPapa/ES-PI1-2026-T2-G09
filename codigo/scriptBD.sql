CREATE DATABASE IF NOT EXISTS PI;
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
       ('Rafael', 12, 'JTPO');


CREATE TABLE eleitores(
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
cpf VARCHAR(11) UNIQUE NOT NULL,
numero_titulo VARCHAR(12) UNIQUE NOT NULL,
mesario BOOLEAN DEFAULT FALSE,
chave_acesso VARCHAR(7) NOT NULL,
status_de_voto BOOLEAN DEFAULT FALSE
);

CREATE TABLE votos(
id INT AUTO_INCREMENT PRIMARY KEY,
protocolo_voto VARCHAR(100) UNIQUE,
voto int,
data_hora DATETIME
);