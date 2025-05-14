import { 
  users, 
  type User, 
  type InsertUser,
  waitlist,
  type Waitlist,
  type InsertWaitlist,
  contacts,
  type Contact,
  type InsertContact
} from "@shared/schema";

// modify the interface with any CRUD methods
// you might need

export interface IStorage {
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Waitlist methods
  addToWaitlist(email: InsertWaitlist): Promise<Waitlist>;
  getWaitlistByEmail(email: string): Promise<Waitlist | undefined>;
  getAllWaitlist(): Promise<Waitlist[]>;
  
  // Contact methods
  createContact(contact: InsertContact): Promise<Contact>;
  getAllContacts(): Promise<Contact[]>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private waitlistEntries: Map<number, Waitlist>;
  private contactEntries: Map<number, Contact>;
  
  private userCurrentId: number;
  private waitlistCurrentId: number;
  private contactCurrentId: number;

  constructor() {
    this.users = new Map();
    this.waitlistEntries = new Map();
    this.contactEntries = new Map();
    
    this.userCurrentId = 1;
    this.waitlistCurrentId = 1;
    this.contactCurrentId = 1;
  }

  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.userCurrentId++;
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }
  
  // Waitlist methods
  async addToWaitlist(insertEmail: InsertWaitlist): Promise<Waitlist> {
    const id = this.waitlistCurrentId++;
    const entry: Waitlist = { 
      ...insertEmail, 
      id, 
      createdAt: new Date().toISOString() 
    };
    this.waitlistEntries.set(id, entry);
    return entry;
  }
  
  async getWaitlistByEmail(email: string): Promise<Waitlist | undefined> {
    return Array.from(this.waitlistEntries.values()).find(
      (entry) => entry.email === email,
    );
  }
  
  async getAllWaitlist(): Promise<Waitlist[]> {
    return Array.from(this.waitlistEntries.values());
  }
  
  // Contact methods
  async createContact(insertContact: InsertContact): Promise<Contact> {
    const id = this.contactCurrentId++;
    const contact: Contact = {
      ...insertContact,
      id,
      createdAt: new Date().toISOString()
    };
    this.contactEntries.set(id, contact);
    return contact;
  }
  
  async getAllContacts(): Promise<Contact[]> {
    return Array.from(this.contactEntries.values());
  }
}

export const storage = new MemStorage();
