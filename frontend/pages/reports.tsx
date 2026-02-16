import Layout from "../components/Layout";
import { useState } from "react";
import api from "../services/api";

export default function Reports() {
  const [items, setItems] = useState<any[]>([]);
  const load = async () => {
    const { data } = await api.get("/reports/metrics", { params: { from_date: "2024-01-01", to_date: "2030-01-01" } });
    setItems(data);
  };

  return <Layout>
    <h1 className="text-2xl font-semibold mb-4">Reports</h1>
    <button className="bg-slate-800 text-white px-3 py-2 mb-4" onClick={load}>Load Metrics</button>
    <div className="bg-white rounded p-3">
      {items.map((item) => <div key={`${item.campaign_id}-${item.date}`} className="border-b py-2 text-sm">Campaign {item.campaign_id} — Impr: {item.impressions} Clicks: {item.clicks} Spend: ₹{item.spend}</div>)}
    </div>
  </Layout>;
}
