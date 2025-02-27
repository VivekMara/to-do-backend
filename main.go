package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	// Define a simple route
	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, darthman!")
	})

	// Start the server
	log.Fatal(app.Listen(":6969"))
}
