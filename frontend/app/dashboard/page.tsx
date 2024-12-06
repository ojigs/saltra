"use client";
import ToastButton from "@/components/toast-button";
import { ToastAction } from "@radix-ui/react-toast";
import { useEffect } from "react";

export default function Dashboard() {
  useEffect(() => {
    console.log("type safety with typescript enabled");
  });
  return (
    <div>
      <h1 className="text-primary">Dashboard</h1>
      <ToastButton
        title="Scheduled: Catch up"
        description="Friday, February 10, 2023 at 5:57 PM"
        action={<ToastAction altText="Try again">Try again</ToastAction>}
        variant={"destructive"}
      >
        Show Toast
      </ToastButton>
    </div>
  );
}
