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

-- Registra que um cliente entrou em contato com um profissional.
-- status: 'iniciado' (acabou de contatar) ou 'concluido' (o cliente marcou que o serviço terminou).
CREATE TABLE IF NOT EXISTS contatos (
    id_contato      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente      INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_profissional INTEGER NOT NULL REFERENCES profissionais(id_profissional),
    data_contato    TEXT NOT  NULL DEFAULT (datetime('now', '-3 hours')),
    status          TEXT NOT NULL DEFAULT 'iniciado' CHECK (status IN ('iniciado', 'concluido'))
);


-- Uma avaliação por contato (o UNIQUE em id_contato garante isso).
CREATE TABLE IF NOT EXISTS avaliacoes (
    id_avaliacao          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contato            INTEGER NOT NULL UNIQUE REFERENCES contatos(id_contato),
    id_cliente            INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_profissional       INTEGER NOT NULL REFERENCES profissionais(id_profissional),
    nota                  INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
    comentario            TEXT NOT NULL,
    resposta_profissional TEXT,
    data_avaliacao        TEXT NOT NULL DEFAULT (datetime('now', '-3 hours'))
);
