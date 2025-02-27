package handlers

import (
	"github.com/gofiber/fiber/v2"
	"to-do-backend/config"
)

// Get all users from the database
func GetUsers(c *fiber.Ctx) error {
	var users []database.User
	database.DB.Find(&users)
	return c.JSON(users)
}

// Get a single user by ID
func GetUserByID(c *fiber.Ctx) error {
	id := c.Params("id")
	var user database.User

	if err := database.DB.First(&user, id).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "User not found"})
	}

	return c.JSON(user)
}

// Create a new user and store in the database
func CreateUser(c *fiber.Ctx) error {
	var user database.User

	if err := c.BodyParser(&user); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid input"})
	}

	database.DB.Create(&user)
	return c.Status(201).JSON(user)
}

// Delete a user by ID
func DeleteUser(c *fiber.Ctx) error {
	id := c.Params("id")
	var user database.User

	if err := database.DB.First(&user, id).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "User not found"})
	}

	database.DB.Delete(&user)
	return c.JSON(fiber.Map{"message": "User deleted"})
}
