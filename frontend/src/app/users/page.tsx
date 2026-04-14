"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface User {
  email: string;
  created_at: string;
  password_reset: boolean;
}

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [resettingEmail, setResettingEmail] = useState<string | null>(null);
  const [resetStatuses, setResetStatuses] = useState<Record<string, string>>({});

  const fetchUsers = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/users`);
      if (!res.ok) throw new Error("Failed to fetch users");
      const data: User[] = await res.json();
      setUsers(data);
    } catch (err) {
      console.error("Error fetching users:", err);
      toast.error("Failed to load users. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleResetPassword = async (email: string) => {
    setResettingEmail(email);
    setResetStatuses((prev) => ({ ...prev, [email]: "" }));

    try {
      const res = await fetch(`${API_URL}/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();

      if (!res.ok) {
        setResetStatuses((prev) => ({
          ...prev,
          [email]: `Error: ${data.detail || "Failed"}`,
        }));
        toast.error(`Failed to reset password for ${email}`);
        return;
      }

      setResetStatuses((prev) => ({
        ...prev,
        [email]: "Password reset successful!",
      }));
      toast.success(`Password reset for ${email}`);

      // Refresh users to update the password_reset status
      await fetchUsers();
    } catch (err) {
      console.error("Error resetting password:", err);
      setResetStatuses((prev) => ({
        ...prev,
        [email]: "Error: Network error",
      }));
      toast.error("Network error. Is the backend running?");
    } finally {
      setResettingEmail(null);
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold tracking-tight">Users</h1>
        <p className="text-muted-foreground mt-1">
          Manage users and reset passwords.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Users</CardTitle>
          <CardDescription>
            {loading
              ? "Loading..."
              : `${users.length} user${users.length !== 1 ? "s" : ""} found`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-12 text-muted-foreground">
              Loading users...
            </div>
          ) : users.length === 0 ? (
            <div className="flex items-center justify-center py-12 text-muted-foreground">
              No users found. Create one first.
            </div>
          ) : (
            <Table data-testid="users-table">
              <TableHeader>
                <TableRow>
                  <TableHead>Email</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.email} data-testid={`user-row-${user.email}`}>
                    <TableCell className="font-medium">{user.email}</TableCell>
                    <TableCell className="text-muted-foreground">
                      {new Date(user.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      {user.password_reset ? (
                        <Badge variant="outline" className="text-amber-600 border-amber-300">
                          Password Reset
                        </Badge>
                      ) : (
                        <Badge variant="secondary">Active</Badge>
                      )}
                    </TableCell>
                    <TableCell className="text-right space-x-2">
                      <Button
                        variant="destructive"
                        size="sm"
                        disabled={resettingEmail === user.email}
                        onClick={() => handleResetPassword(user.email)}
                        data-testid={`reset-btn-${user.email}`}
                      >
                        {resettingEmail === user.email
                          ? "Resetting..."
                          : "Reset Password"}
                      </Button>

                      {/* Status feedback for Playwright agent */}
                      {resetStatuses[user.email] && (
                        <span
                          className="text-sm text-muted-foreground ml-2"
                          data-testid={`reset-status-${user.email}`}
                        >
                          {resetStatuses[user.email]}
                        </span>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
