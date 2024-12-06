"use client";

import { FC } from "react";
import { cn } from "@/lib/utils";
import { Button } from "./ui/button";
import { ToastButtonProps } from "@/lib/definitions";
import { useToast } from "@/hooks/use-toast";

const ToastButton: FC<ToastButtonProps> = ({
  title,
  description,
  variant,
  action,
  className,
  ...buttonProps
}) => {
  const { toast } = useToast();
  return (
    <Button
      {...buttonProps}
      className={cn(``, { className })}
      onClick={() => {
        toast({
          title,
          description,
          variant,
          action,
        });
      }}
    ></Button>
  );
};

export default ToastButton;
