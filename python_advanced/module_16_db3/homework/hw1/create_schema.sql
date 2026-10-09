
PRAGMA foreign_keys = ON;

CREATE TABLE actors (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_last_name VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL)
);


CREATE TABLE movie (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
);


CREATE TABLE director (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL,
    dir_last_name VARCHAR(50) NOT NULL
);


CREATE TABLE movie_cast (
    act_id INTEGER NOT NULL,
    mov_id INTEGER NOT NULL,
    role VARCHAR(50),
    PRIMARY KEY (act_id, mov_id),
    FOREIGN KEY (act_id) REFERENCES actors(act_id)
        ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
        ON DELETE CASCADE
);

CREATE TABLE oscar_awarded (
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER NOT NULL,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
        ON DELETE CASCADE
);


CREATE TABLE movie_direction (
    dir_id INTEGER NOT NULL,
    mov_id INTEGER NOT NULL,
    PRIMARY KEY (dir_id, mov_id),
    FOREIGN KEY (dir_id) REFERENCES director(dir_id)
        ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
        ON DELETE CASCADE
);