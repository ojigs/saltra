// "use client";
import { getAllLeads } from "@/lib/data";

export default async function Leads({
  searchParams,
}: {
  searchParams?: {
    query?: string;
    page?: string;
  };
}) {
  const query = searchParams?.query || "";
  {
    const leads = await getAllLeads();

    console.log("are you active??");

    console.log(`Leads: ${leads}`);
    return (
      <div className="container mx-4">
        <h1>Leads</h1>
        <p>Talk about yourself in a few words...</p>
        <div className="flex flex-col gap-2">
          {leads.map((lead) => (
            <span key={lead.id}>{lead.status}</span>
          ))}
        </div>
      </div>
    );
  }
}
