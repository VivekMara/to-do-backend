package main

import (
	"log"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2"
	"to-do-backend/routes"
	"to-do-backend/config"
)

func main() {
	database.ConnectDatabase()
	app := fiber.New()

	app.Use(logger.New()) // Logs each request
	app.Use(cors.New())   // Enables CORS

	routes.SetupRoutes(app)

	// Start the server
	log.Fatal(app.Listen(":6969"))
}
