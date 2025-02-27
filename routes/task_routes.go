package routes

import (
	"github.com/gofiber/fiber/v2"
	"to-do-backend/handlers" // Import handlers
)

// SetupRoutes initializes all routes
func SetupRoutes(app *fiber.App) {
	api := app.Group("/api") // Base route group

	api.Get("/users", handlers.GetUsers)
	api.Get("/users/:id", handlers.GetUserByID)
	api.Post("/users", handlers.CreateUser)
	api.Delete("/users/:id", handlers.DeleteUser)
}
