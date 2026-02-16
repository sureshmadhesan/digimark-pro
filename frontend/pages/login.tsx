import { useState } from "react";
import { useRouter } from "next/router";
import api from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const submit = async () => {
    setError("");
    if (!email || !password) return setError("Email and password are required.");
    try {
      const { data } = await api.post("/auth/login", { email, password });
      localStorage.setItem("accessToken", data.access_token);
      router.push("/");
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-white p-6 rounded shadow">
      <h1 className="text-xl font-semibold mb-4">Login</h1>
      <input className="border p-2 w-full mb-3" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input className="border p-2 w-full mb-3" type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
      <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={submit}>Sign in</button>
    </div>
  );
}
