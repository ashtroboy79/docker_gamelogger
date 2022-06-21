CREATE TABLE IF NOT EXISTS gamer (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS game (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    designer VARCHAR(50),
    genre VARCHAR(50),
    rating INT,
    gamer_id INT NOT NULL,
    FOREIGN KEY (gamer_id) REFERENCES gamer(id)
);
