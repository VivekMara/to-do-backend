package database

import (
	"log"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// DB is a global variable to access the database
var DB *gorm.DB

// ConnectDatabase initializes the SQLite database
func ConnectDatabase() {
	var err error
	DB, err = gorm.Open(sqlite.Open("db/users.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	log.Println("Connected to the database!")

	// Auto-migrate the User struct (create the table if not exists)
	DB.AutoMigrate(&User{})
}

// User model for the database
type User struct {
	ID   uint   `gorm:"primaryKey;autoIncrement"`
	Name string `json:"name"`
}
