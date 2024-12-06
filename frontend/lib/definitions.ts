import { ButtonProps } from "@/components/ui/button";
import { ToastActionElement } from "@/components/ui/toast";

export interface ToastButtonProps extends ButtonProps {
  action?: ToastActionElement;
  title: string;
  description?: string;
  className?: string;
  variant?: "default" | "destructive" | null | undefined;
}

export enum LeadSource {
  WEBSITE = "website",
  LINKEDIN = "linkedin",
  CONFERENCE = "conference",
  COLD_EMAIL = "cold_email",
  REFERRAL = "referral",
  OTHER = "Other",
}

export enum LeadStatus {
  NEW = "new",
  CONTACTED = "contacted",
  QUALIFIED = "qualified",
  NEGOTIATION = "negotiation",
  CLOSED_WON = "closed_won",
  CLOSED_LOST = "closed_lost",
}

export type InteractionType =
  | "email"
  | "call"
  | "meeting"
  | "demo"
  | "follow-up";

export type LeadCategory = "Premium" | "Hot" | "Warm" | "Cold";

export interface Interaction {
  date: string;
  type: InteractionType;
  notes?: string;
  owner: string;
}

export interface LeadBase {
  id?: string;
  first_name: string;
  last_name: string;
  company: string;
  company_size: number;
  email: string;
  job_title?: string;
  phone?: string;
  source: LeadSource;
  status: LeadStatus;
  interactions?: Interaction[];
}

export interface LeadModel extends LeadBase {
  score: number;
  category?: LeadCategory;
  created_at: string;
  updated_at: string;
}

export interface LeadUpdateSchema {
  first_name?: string;
  last_name?: string;
  company?: string;
  company_size?: number;
  email?: string;
  job_title?: string;
  phone?: string;
  source?: LeadSource;
  status?: LeadStatus;
}

export interface LeadListSchema {
  leads: LeadModel[];
}

export const LeadValidation = {
  firstName: {
    minLength: 2,
    maxLength: 100,
  },
  lastName: {
    minLength: 2,
    maxLength: 100,
  },
  company: {
    minLength: 2,
    maxLength: 100,
  },
  companySize: {
    min: 1,
  },
  score: {
    min: 0,
    max: 100,
  },
  phone: {
    pattern: /^\+?[0-9]{1,15}$/,
  },
};
