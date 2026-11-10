--  Tabelas da Sprint 1 (versão SQLite)

-- Lista de bairros de teresina. A "zona" serve para sugerir bairros próximos.
CREATE TABLE IF NOT EXISTS bairros(
    id_bairro INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_bairro TEXT NOT NULL UNIQUE,
    zona TEXT NOT NULL CHECK (zona IN ('Sul', 'Leste', 'Norte', 'Sudeste', 'Central'))
);

-- Tipos de serviço. Usada no cadastro e no filtro da busca.
CREATE TABLE IF NOT EXISTS categorias_servico (
    id_categoria   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL UNIQUE
);

-- Dados de login comuns a clientes e profissionais.
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    senha_hash    TEXT NOT NULL,
    telefone      TEXT NOT NULL,
    tipo_usuario  TEXT NOT NULL CHECK (tipo_usuario IN ('cliente', 'profissional', 'admin')),
    data_cadastro TEXT NOT NULL DEFAULT (datetime('now', '-3 hours')),  -- hora de Teresina (UTC-3)
    status        TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'banido'))
);

-- Dados so do cliente. O bairro é opcional
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario   INTEGER NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_bairro    INTEGER  REFERENCES bairros(id_bairro)       
);


-- Dados só do profissional. Por enquanto: 1 bairro e 1 categoria por profissional.
CREATE TABLE IF NOT EXISTS profissionais (
    id_profissional      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario           INTEGER NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_bairro            INTEGER NOT NULL REFERENCES bairros(id_bairro),
    id_categoria         INTEGER NOT NULL REFERENCES categorias_servico(id_categoria),
    descricao            TEXT,
    disponivel           INTEGER NOT NULL DEFAULT 1,
    documento_verificado INTEGER NOT NULL DEFAULT 0,
    nota_media           REAL DEFAULT 0.0
);
