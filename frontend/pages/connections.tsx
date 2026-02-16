import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";

export default function Connections() {
  const [code, setCode] = useState("");
  const connectGoogle = async () => await api.post("/oauth/google/callback", null, { params: { code, account_id: "123-456-7890" } });
  const connectMeta = async () => await api.post("/oauth/meta/callback", null, { params: { code, ad_account_id: "123456789" } });

  return <Layout>
    <h1 className="text-2xl font-semibold mb-4">Ad Account Connections</h1>
    <input className="border p-2 w-full mb-3" placeholder="Paste OAuth Code" value={code} onChange={(e)=>setCode(e.target.value)} />
    <div className="flex gap-2">
      <button className="bg-red-500 text-white px-4 py-2" onClick={connectGoogle}>Connect Google</button>
      <button className="bg-blue-500 text-white px-4 py-2" onClick={connectMeta}>Connect Meta</button>
    </div>
  </Layout>;
}
