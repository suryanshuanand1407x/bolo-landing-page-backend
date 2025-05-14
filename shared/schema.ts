import { z } from "zod";

// Insert Schemas
export const insertUserSchema = z.object({
  username: z.string(),
  password: z.string()
});

export const insertWaitlistSchema = z.object({
  email: z.string().email()
});

export const insertContactSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  message: z.string()
});

// Types
export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = {
  id: number;
  username: string;
  password: string;
};

export type InsertWaitlist = z.infer<typeof insertWaitlistSchema>;
export type Waitlist = {
  id: number;
  email: string;
  createdAt: string;
};

export type InsertContact = z.infer<typeof insertContactSchema>;
export type Contact = {
  id: number;
  name: string;
  email: string;
  message: string;
  createdAt: string;
};
