DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Guest;
DROP TABLE IF EXISTS LicensePlate;
DROP TABLE IF EXISTS Rates;
DROP TABLE IF EXISTS Parking;


CREATE TABLE User (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Username TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL
);


CREATE TABLE Member (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  RFID TEXT UNIQUE NOT NULL,
  LastName TEXT NOT NULL,
  FirstName TEXT NOT NULL,
  Phone TEXT NOT NULL,
  Email TEXT UNIQUE NOT NULL,
  isPayed BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE Guest (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Code TEXT NOT NULL
);


CREATE TABLE LicensePlate (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  PlateNumber TEXT NOT NULL,
  EntryDate DATETIME,
  ExitDate DATETIME,
  MemberID INTEGER,
  GuestID INTEGER,
  FOREIGN KEY (MemberID) REFERENCES Member(ID),
  FOREIGN KEY (GuestID) REFERENCES Guest(ID)
);


CREATE TABLE Rates (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Duration INTEGER NOT NULL,  -- Durée en minutes
  Price DECIMAL(5,2) NOT NULL -- Prix en devise locale
);


CREATE TABLE Parking (
  PlaceID TEXT PRIMARY KEY,    -- Identifiants 'a', 'b', 'c', 'd' pour les places
  isEmpty BOOLEAN NOT NULL,    -- True si la place est vide, False sinon
  LicensePlateID INTEGER,      -- Optionnel, ID de la plaque si la place est occupée
  FOREIGN KEY (LicensePlateID) REFERENCES LicensePlate(ID)
);

INSERT INTO Parking (PlaceID, isEmpty, LicensePlateID) VALUES
('a', TRUE, NULL),
('b', TRUE, NULL),
('c', TRUE, NULL),
('d', TRUE, NULL);

