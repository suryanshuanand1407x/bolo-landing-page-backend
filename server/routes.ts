import type { Express, Request, Response } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { 
  insertWaitlistSchema, 
  insertContactSchema
} from "@shared/schema";
import { z } from "zod";
import { fromZodError } from "zod-validation-error";

export async function registerRoutes(app: Express): Promise<Server> {
  // API endpoints for waitlist and contact forms
  
  // Add email to waitlist
  app.post("/api/waitlist", async (req: Request, res: Response) => {
    try {
      // Validate request body
      const validatedData = insertWaitlistSchema.parse(req.body);
      
      // Check if email already exists
      const existingEntry = await storage.getWaitlistByEmail(validatedData.email);
      if (existingEntry) {
        return res.status(409).json({
          message: "This email is already on our waitlist",
        });
      }
      
      // Add to waitlist
      const result = await storage.addToWaitlist(validatedData);
      return res.status(201).json({
        message: "Successfully added to waitlist",
        id: result.id,
      });
    } catch (error) {
      if (error instanceof z.ZodError) {
        const validationError = fromZodError(error);
        return res.status(400).json({
          message: validationError.message,
        });
      }
      
      return res.status(500).json({
        message: "An unexpected error occurred",
      });
    }
  });
  
  // Submit contact form
  app.post("/api/contact", async (req: Request, res: Response) => {
    try {
      // Validate request body
      const validatedData = insertContactSchema.parse(req.body);
      
      // Save contact message
      const result = await storage.createContact(validatedData);
      return res.status(201).json({
        message: "Message sent successfully",
        id: result.id,
      });
    } catch (error) {
      if (error instanceof z.ZodError) {
        const validationError = fromZodError(error);
        return res.status(400).json({
          message: validationError.message,
        });
      }
      
      return res.status(500).json({
        message: "An unexpected error occurred",
      });
    }
  });
  
  // Get all waitlist entries (for admin purposes)
  app.get("/api/waitlist", async (req: Request, res: Response) => {
    try {
      const entries = await storage.getAllWaitlist();
      return res.status(200).json(entries);
    } catch (error) {
      return res.status(500).json({
        message: "An unexpected error occurred",
      });
    }
  });
  
  // Get all contact messages (for admin purposes)
  app.get("/api/contact", async (req: Request, res: Response) => {
    try {
      const messages = await storage.getAllContacts();
      return res.status(200).json(messages);
    } catch (error) {
      return res.status(500).json({
        message: "An unexpected error occurred",
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
