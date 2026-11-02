--  Tabelas da Sprint 1 (versão SQLite)

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    senha_hash    TEXT NOT NULL,
    telefone      TEXT NOT NULL,
    tipo_usuario  TEXT NOT NULL CHECK (tipo_usuario IN ('cliente', 'profissional', 'admin')),
    latitude      REAL,
    longitude     REAL,
    data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status        TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'banido'))
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario          INTEGER NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    endereco_referencia TEXT
);

CREATE TABLE IF NOT EXISTS profissionais (
    id_profissional      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario           INTEGER NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    endereco_referencia  TEXT,
    categoria            TEXT,  -- provisório: depois vira categorias_servico
    descricao            TEXT,
    disponivel           INTEGER NOT NULL DEFAULT 1,
    documento_verificado INTEGER NOT NULL DEFAULT 0,
    nota_media           REAL DEFAULT 0.0
);