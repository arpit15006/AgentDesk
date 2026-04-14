"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CreateUserPage() {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email.trim()) {
      toast.error("Please enter an email address");
      return;
    }

    setIsSubmitting(true);
    setStatusMessage("");

    try {
      const res = await fetch(`${API_URL}/create-user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });

      const data = await res.json();

      if (!res.ok) {
        setStatusMessage(`Error: ${data.detail || "Failed to create user"}`);
        toast.error(data.detail || "Failed to create user");
        return;
      }

      setStatusMessage(`User ${email.trim()} created successfully!`);
      toast.success(`User ${email.trim()} created!`);
      setEmail("");
    } catch (err) {
      console.error("Error creating user:", err);
      setStatusMessage("Error: Network error");
      toast.error("Network error. Is the backend running?");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight">Create User</h1>
        <p className="text-muted-foreground mt-1">
          Add a new user to the system.
        </p>
      </div>

      <Card className="max-w-lg">
        <CardHeader>
          <CardTitle>New User</CardTitle>
          <CardDescription>
            Enter the email address to create a new user account.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label
                htmlFor="email-input"
                className="text-sm font-medium leading-none"
              >
                Email Address
              </label>
              <Input
                id="email-input"
                type="email"
                placeholder="user@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isSubmitting}
                data-testid="email-input"
              />
            </div>

            <Button
              type="submit"
              disabled={isSubmitting}
              data-testid="create-btn"
            >
              {isSubmitting ? "Creating..." : "Create User"}
            </Button>

            {/* Status feedback for Playwright agent */}
            {statusMessage && (
              <p
                className={`text-sm mt-2 ${
                  statusMessage.startsWith("Error")
                    ? "text-destructive"
                    : "text-green-600"
                }`}
                data-testid="create-status"
              >
                {statusMessage}
              </p>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
