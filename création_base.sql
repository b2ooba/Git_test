-- Création de la table pour les utilisateurs
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL
);

-- Création de la table pour les conversations
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);

-- Création de la table pour les participants aux conversations
CREATE TABLE participants (
    utilisateur_id INT REFERENCES utilisateurs(id),
    conversation_id INT REFERENCES conversations(id),
    PRIMARY KEY (utilisateur_id, conversation_id)
);

-- Création de la table pour les messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    contenu TEXT NOT NULL,
    utilisateur_id INT REFERENCES utilisateurs(id),
    conversation_id INT REFERENCES conversations(id),
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
