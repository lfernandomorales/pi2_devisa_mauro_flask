DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS avaliacoes;

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created DATE,
  updated DATE,
  title VARCHAR NOT NULL,
  links VARCHAR NOT NULL,
  details TEXT NOT NULL,
  status_evento VARCHAR NOT NULL, 
  clipping BOOLEAN,
  cme BOOLEAN,
  data_insercao_no_clipping DATE, 
  ultima_data_no_clipping DATE, 
  data_inicio_monitoramento_no_cme DATE, 
  data_encerramento_do_monitaramento DATE, 
  ultima_avaliacao_risco VARCHAR,
  compartilhamento_da_informacao BOOLEAN 
);

CREATE TABLE avaliacoes (
	id INTEGER NOT NULL, 
	data_da_avaliacao DATE NOT NULL, 
	avaliado_por VARCHAR, 
	avaliacao01 INTEGER, 
	avaliacao02 INTEGER, 
	avaliacao03 INTEGER, 
	avaliacao04 INTEGER, 
	avaliacao05 INTEGER, 
	avaliacao06 INTEGER, 
	avaliacao07 INTEGER, 
	avaliacao08 INTEGER, 
	avaliacao09 INTEGER, 
	avaliacao10 INTEGER, 
	avaliacao11 INTEGER, 
	avaliacao12 INTEGER, 
	avaliacao13 INTEGER, 
	avaliacao14 INTEGER, 
	avaliacao15 INTEGER, 
	avaliacao16 INTEGER, 
	avaliacao17 INTEGER, 
	avaliacao18 INTEGER, 
	avaliacao19 INTEGER, 
	avaliacao20 INTEGER, 
	avaliacao21 INTEGER, 
	probabilidade INTEGER, 
	impacto_saude_humana INTEGER, 
	impacto_na_assistencia INTEGER, 
	impacto_social INTEGER, 
	impacto_na_capacidade_de_resposta INTEGER, 
	avaliacao_de_risco VARCHAR, 
	PRIMARY KEY (id, data_da_avaliacao), 
	FOREIGN KEY(id) REFERENCES posts (id)
);

/*
 DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
*/
