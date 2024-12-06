import { useToast } from "@/hooks/use-toast";
import { unstable_noStore as noStore } from "next/cache";
import { LeadListSchema } from "./definitions";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchData<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  //   const { toast } = useToast();
  const defaultOptions: RequestInit = {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);

    if (!response.ok) {
      throw new Error(`Failed to fetch ${endpoint}: ${response.statusText}`);
    }

    const data = await response.json();

    return data;

    // return await response.json();
  } catch (error: unknown) {
    console.error(`Error fetching data from ${url}:`, error);
    // toast({ title: "Error", description: (error as Error).message });
    throw error;
  }
}

// get dashboard stats
export async function getDashboardStats() {
  return await fetchData<{
    totalLeads: number;
    newLeads: number;
    hotLeads: number;
    conversionRate: number;
  }>("/dashboard/stats");
}

// get all leads
export async function getAllLeads() {
  noStore();
  const { leads } = await fetchData<LeadListSchema>("/leads");
  return leads;
}

// get lead by id
export async function getLeadDetails(leadId: string) {
  noStore();
  return await fetchData<{
    id: string;
    name: string;
    email: string;
    phone?: string;
    status: string;
    interactionHistory: Array<{
      date: string;
      note: string;
    }>;
  }>(`/leads/${leadId}`);
}

// get leads analytics
export async function getAnalyticsData() {
  return await fetchData<{
    leadScoringDistribution: Array<{ score: number; count: number }>;
    sourceBreakdown: Array<{ source: string; count: number }>;
    conversionRates: Array<{ stage: string; percentage: number }>;
  }>("/analytics");
}

export async function getUserProfile() {
  return await fetchData<{
    id: string;
    name: string;
    email: string;
    avatarUrl?: string;
  }>("/settings/profile");
}
