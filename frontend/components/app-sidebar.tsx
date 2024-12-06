"use client";

import * as React from "react";
import {
  AudioWaveform,
  Home,
  ChartNoAxesColumn,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  Settings,
  SquareTerminal,
  Users,
  LayoutGrid,
  ChartNoAxesCombined,
} from "lucide-react";
import { NavMain } from "@/components/nav-main";
import { NavUser } from "@/components/nav-user";
import { TeamSwitcher } from "@/components/team-switcher";
// import { SaltraLogo } from "./dashboard/saltra-logo";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar";
// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Saltra",
      logo: GalleryVerticalEnd,
      plan: "Sales Tracker",
    },
  ],
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: LayoutGrid,
      isActive: true,
      items: [
        {
          title: "History",
          url: "#",
        },
        {
          title: "Starred",
          url: "#",
        },
        {
          title: "Settings",
          url: "#",
        },
      ],
    },
    {
      title: "Leads",
      url: "/dashboard/leads",
      icon: Users,
      items: [
        {
          title: "Genesis",
          url: "#",
        },
        {
          title: "Explorer",
          url: "#",
        },
        {
          title: "Quantum",
          url: "#",
        },
      ],
    },
    {
      title: "Analytics",
      url: "/dashboard/analytics",
      icon: ChartNoAxesCombined,
      items: [
        {
          title: "Introduction",
          url: "#",
        },
        {
          title: "Get Started",
          url: "#",
        },
        {
          title: "Tutorials",
          url: "#",
        },
        {
          title: "Changelog",
          url: "#",
        },
      ],
    },
    {
      title: "Settings",
      url: "/dashboard/settings",
      icon: Settings,
      items: [
        {
          title: "General",
          url: "#",
        },
        {
          title: "Team",
          url: "#",
        },
        {
          title: "Billing",
          url: "#",
        },
        {
          title: "Limits",
          url: "#",
        },
      ],
    },
  ],
  projects: [
    {
      name: "Design Engineering",
      url: "#",
      icon: Frame,
    },
    {
      name: "Sales & Marketing",
      url: "#",
      icon: PieChart,
    },
    {
      name: "Travel",
      url: "#",
      icon: Map,
    },
  ],
};
export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}

// ("use client");

// import {
//   Sidebar,
//   SidebarHeader,
//   SidebarContent,
//   SidebarTrigger,
// } from "@/components/ui/sidebar";
// import { HomeIcon, UsersIcon, BarChartIcon, SettingsIcon } from "lucide-react";
// import Link from "next/link";

// const navigation = [
//   { href: "/", label: "Dashboard", icon: <HomeIcon className="w-5 h-5" /> },
//   { href: "/leads", label: "Leads", icon: <UsersIcon className="w-5 h-5" /> },
//   {
//     href: "/analytics",
//     label: "Analytics",
//     icon: <BarChartIcon className="w-5 h-5" />,
//   },
//   {
//     href: "/settings",
//     label: "Settings",
//     icon: <SettingsIcon className="w-5 h-5" />,
//   },
// ];

// export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
//   return (
//     <Sidebar>
//       {/* Sidebar Trigger */}
//       {/* <SidebarTrigger>
//         <button className="p-2">
//           <span className="sr-only">Toggle Sidebar</span>
//         </button>
//       </SidebarTrigger> */}

//       {/* Sidebar Header */}
//       <SidebarHeader>
//         <Link href="/" className="text-lg font-bold text-indigo-600">
//           SalesApp
//         </Link>
//       </SidebarHeader>

//       {/* Sidebar Content */}
//       <SidebarContent>
//         <nav className="flex flex-col gap-4">
//           {navigation.map((item) => (
//             <Link
//               key={item.href}
//               href={item.href}
//               className="flex items-center gap-3 p-2 rounded-md hover:bg-indigo-50 hover:text-indigo-600"
//             >
//               {item.icon}
//               <span>{item.label}</span>
//             </Link>
//           ))}
//         </nav>
//       </SidebarContent>
//     </Sidebar>
//   );
// }

// import { Home, Inbox, Calendar, Settings, User } from "lucide-react";
// import Link from "next/link";
// import {
//   Sidebar,
//   SidebarContent,
//   SidebarFooter,
//   SidebarGroup,
//   SidebarGroupLabel,
//   SidebarHeader,
//   SidebarMenu,
//   SidebarMenuButton,
//   SidebarMenuItem,
//   SidebarRail,
// } from "@/components/ui/sidebar";
// import NavLinks from "./nav-links";

// const items = [
//   {
//     title: "Dashboard",
//     url: "/",
//     icon: Home,
//   },
//   {
//     title: "Leads",
//     url: "/leads",
//     icon: Inbox,
//   },
//   {
//     title: "Analytics",
//     url: "/analytics",
//     icon: Calendar,
//   },
//   {
//     title: "Settings",
//     url: "/settings",
//     icon: Settings,
//   },
//   {
//     title: "Login",
//     url: "/auth/login",
//     icon: User,
//   },
//   {
//     title: "Signup",
//     url: "/auth/signup",
//     icon: User,
//   },
// ];

// export function AppSidebar() {
//   return (
//     <Sidebar>
//       <SidebarContent>
//         <SidebarHeader>
//           <Link href="/" className="text-lg font-bold text-indigo-600">
//             Saltra
//           </Link>
//         </SidebarHeader>
//         <SidebarGroup>
//           <SidebarGroupLabel>Platform</SidebarGroupLabel>
//           <SidebarMenu>
//             <NavLinks />
//           </SidebarMenu>
//         </SidebarGroup>
//       </SidebarContent>
//     </Sidebar>
//   );
// }
