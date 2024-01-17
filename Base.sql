-- Supprime les tables si elles existent
drop table if exists conversations;
drop table if exists friends;
drop table if exists users;

-- Crée la table des utilisateurs
create table users (
       id_user serial primary key,
       username varchar(20),
       password varchar(20)
);

-- Crée la table des amis
create table friends (
       id_friend serial primary key,
       user_id int references users(id_user),
       friend_username varchar(20),
       foreign key (friend_username) references users(username)
);

-- Crée la table des conversations
create table conversations (
       id_conversation serial primary key,
       user1_id int references users(id_user),
       user2_id int references users(id_user),
       foreign key (user1_id) references users(id_user),
       foreign key (user2_id) references users(id_user)
);

-- Crée la table des messages
create table messages (
       id_message serial primary key,
       conversation_id int references conversations(id_conversation),
       sender_id int references users(id_user),
       message_text varchar(255),
       foreign key (conversation_id) references conversations(id_conversation),
       foreign key (sender_id) references users(id_user)
);

CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
);
